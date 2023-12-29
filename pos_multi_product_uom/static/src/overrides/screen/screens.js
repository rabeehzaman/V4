/*@odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
const { DateTime } = luxon;
import { serializeDateTime } from "@web/core/l10n/dates";

// Unit Selection Popup----------------

export class UnitSelectionPopupWidget extends AbstractAwaitablePopup {
  static template = "UnitSelectionPopupWidget";
  setup() {
    super.setup();
    var self = this;
    self.item = '';
    self.value = '' || self.props.value;
    self.props.is_selected = self.props.is_selected || false;
    self.list = self.props.list || [];
    for (var key in self.list) {
      self.list[key].selected = false;
      if (self.list[key].item == self.value) {
        self.list[key].selected = self;
      }
    }
    this.render();
    console.log("popup setup", this)
  }
  click_item(event) {
    var self = this;
    var item = this.props.list[parseInt($(event.target).data('item-index'))];
    item = item ? item.item : item;
    this.item = item;
    for (var el in this.props.list) {
      this.props.list[el].selected = false;
    }
    this.props.list[parseInt($(event.target).data('item-index'))].selected = true;
    if (item == this.value) {
      this.props.is_selected = false;
    } else {
      $(event.target).addClass("selected")
      this.props.is_selected = true;
    }
    this.render();
  }

  click_confirm(event) {
    var self = this;
    self.props.orderline.set_unit(self.item);
    var pricelist = self.env.services.pos.get_order().pricelist;
    var unit_price = self.props.orderline.price;
    console.log(pricelist)
    var quantity = (this.env.services.pos.units_by_id[self.item].ratio);
    var ratio = self.props.orderline.get_unit().ratio;
    var orderline_quantitys;
    if (quantity < 1) {
      orderline_quantitys = self.props.orderline.quantity;
    } else {
      orderline_quantitys = quantity * self.props.orderline.quantity;
    }
    var price = self.props.orderline.wk_get_price(pricelist, orderline_quantitys, unit_price);
    if (self.props.orderline.product.uom_id[0] !== self.props.orderline.uom_id) {
      var price = self.props.orderline.product.get_price(pricelist, orderline_quantitys, self.props.orderline.get_price_extra())
      var multiply = self.check_pricelist(pricelist, orderline_quantitys, self.props.orderline.product)
      if (!multiply) {
        self.props.orderline.price = (price * quantity)
      } else {
        self.props.orderline.price = price
      }
    } else {
      var price = self.props.orderline.product.get_price(pricelist, orderline_quantitys, self.props.orderline.get_price_extra())
      self.props.orderline.price = price;
    }
    // self.props.orderline.set_unit(self.item);
    this.cancel();
  }
  check_pricelist(pricelist, quantity, product) {
    var self = this;
    var date = luxon.DateTime.now()
    if (pricelist === undefined) {
      return false
    }
    var category_ids = [];
    var category = product.categ;
    while (category) {
      category_ids.push(category.id);
      category = category.parent;
    }
    var pricelist_items = pricelist.items.filter(function (item) {
      return (!item.product_tmpl_id || item.product_tmpl_id[0] === self.product_tmpl_id) &&
        (!item.product_id || item.product_id[0] === self.id) &&
        (!item.categ_id || _.contains(category_ids, item.categ_id[0])) &&
        (!item.date_start || serializeDateTime(item.date_start).isSameOrBefore(date)) &&
        (!item.date_end || serializeDateTime(item.date_end).isSameOrAfter(date));
    });
    pricelist_items.find(function (rule) {
      if (rule.min_quantity && quantity < rule.min_quantity) {
        return false;
      }
      if (rule.compute_price === 'fixed') {
        return true;
      }
      return false;
    });
    return false;
  }
}

patch(Orderline.prototype, {

  open_UnitSelection_popup() {
    var self = this;
    var categ = [];
    for (var key in self.env.services.pos.units_by_id) {
      if (self.env.services.pos.units_by_id[key].category_id[1] === self.props.line.orderline.get_unit().category_id[1]) {
        categ.push({ item: self.env.services.pos.units_by_id[key].id, label: self.env.services.pos.units_by_id[key].display_name, selected: false });
      }
    }
    self.env.services.popup.add(UnitSelectionPopupWidget, {
      title: "Select Unit of Measure",
      list: categ,
      value: self.props.line.orderline.get_unit().id,
      orderline: self.props.line.orderline
    });
  }
})