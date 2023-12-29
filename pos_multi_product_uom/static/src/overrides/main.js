/*@odoo-module*/

/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */


import { Orderline, Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { parseFloat as oParseFloat } from "@web/views/fields/parsers";

const { DateTime } = luxon;
import { serializeDateTime, deserializeDate } from "@web/core/l10n/dates";
import {
  formatFloat,
  roundDecimals as round_di,
  roundPrecision as round_pr,
  floatIsZero,
} from "@web/core/utils/numbers";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
patch(Orderline.prototype, {
  init_from_JSON(json) {
    super.init_from_JSON(...arguments);
    this.uom_id = json.uom_id;
  },
  get_unit() {
    var unit = super.get_unit(this);
    if (!this.uom_id) {
      return unit;
    }
    var unit_id = this.uom_id;
    return this.pos.units_by_id[unit_id];
  },
  set_unit(unit) {
    this.uom_id = unit;
    // this.trigger('change', this);
  },
  set_unit_price(price) {
    var self = this;
    console.log("set_unit_price", price)
    if (!this.uom_id) {
      super.set_unit_price(price);
    } else {
      if (this.product.uom_id[0] !== this.uom_id) {
        if (!this.do_not_update) {
          var pricelist = this.order.pricelist;
          var quantity = this.quantity;
          // var product_price = (price * this.pos.units_by_id[this.product.uom_id[0]].factor) / this.get_unit().factor;
          var quantity_by_factor = quantity * this.pos.units_by_id[this.product.uom_id[0]].factor / this.get_unit().factor;
          var qty = this.pos.units_by_id[this.product.uom_id[0]].factor / this.get_unit().factor;
          var wk_price = self.wk_get_price(pricelist, quantity_by_factor, 0);
          var multiply = self.check_pricelist(pricelist, quantity_by_factor, this.product)
          if (!multiply) {
            var uom_price = wk_price * qty;
          } else {
            var uom_price = wk_price
          }
          // super.set_unit_price(wk_price * qty);          
          this.order.assert_editable();
          var parsed_price = !isNaN(uom_price) ? uom_price : isNaN(parseFloat(uom_price)) ? 0 : oParseFloat('' + uom_price)
          this.price = round_di(parsed_price || 0, this.pos.dp['Product Price']);
          this.do_not_update = true
        } else {
          this.do_not_update = undefined
        }
      } else {
        super.set_unit_price(price);
      }
    }
  },
  check_pricelist(pricelist, quantity, product) {
    var self = this;
    var date = luxon.DateTime.now();
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
        (!item.categ_id || category_ids.contains(item.categ_id[0])) &&
        (!item.date_start || deserializeDate(item.date_start) <= date) &&
        (!item.date_end || deserializeDate(item.date_end) >= date)
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
  },

  wk_get_price(pricelist, quantity, price_extra) {
    var self = this;
    var date = luxon.DateTime.now();
    var rules = !pricelist
      ? []
      : (this.product.applicablePricelistItems[pricelist.id] || []).filter((item) => {
        return (!item.product_tmpl_id || item.product_tmpl_id[0] === self.product.product_tmpl_id) &&
          (!item.date_start || deserializeDate(item.date_start) <= date) &&
          (!item.date_end || deserializeDate(item.date_end) >= date)
      });
    let price = this.product.lst_price + (price_extra || 0);
    const rule = rules.find((rule) => !rule.min_quantity || quantity >= rule.min_quantity);
    if (!rule) {
      return price;
    }
    if (rule.base === "pricelist") {
      const base_pricelist = this.pos.pricelists.find(
        (pricelist) => pricelist.id === rule.base_pricelist_id[0]
      );
      if (base_pricelist) {
        price = this.wk_get_price(base_pricelist, quantity, 0);
      }
    } else if (rule.base === "standard_price") {
      price = this.product.standard_price;
    }

    if (rule.compute_price === "fixed") {
      price = rule.fixed_price;
    } else if (rule.compute_price === "percentage") {
      price = price - price * (rule.percent_price / 100);
    } else {
      var price_limit = price;
      price -= price * (rule.price_discount / 100);
      if (rule.price_round) {
        price = round_pr(price, rule.price_round);
      }
      if (rule.price_surcharge) {
        price += rule.price_surcharge;
      }
      if (rule.price_min_margin) {
        price = Math.max(price, price_limit + rule.price_min_margin);
      }
      if (rule.price_max_margin) {
        price = Math.min(price, price_limit + rule.price_max_margin);
      }
    }

    return price;
  },
  export_as_JSON() {
    var self = this;
    var pack_lot_ids = super.export_as_JSON(this);
    pack_lot_ids.uom_id = this.get_unit().id;
    return pack_lot_ids;
  },
  getDisplayData() {
    var res = super.getDisplayData()
    res["orderline"] = this
    return res
  },
});
patch(Order.prototype, {
  add_product(product, options) {
    var self = this;
    var result = super.add_product(...arguments)
    if (self.selected_orderline) {
      if (options.unit) {
        var order = self.pos.get_order()
        self.selected_orderline.set_unit(options.unit.id);
        self.selected_orderline.price_manually_set = true;
        order.save_to_db()
      }
    }
    return result
  }
});

patch(TicketScreen.prototype, {
  _prepareRefundOrderlineOptions(toRefundDetail) {
    var result = super._prepareRefundOrderlineOptions(...arguments)
    result.unit = toRefundDetail.orderline.unit
    return result
  },
  _getToRefundDetail(orderline) {
    var result = super._getToRefundDetail(...arguments)
    result.orderline.unit = orderline.get_unit()
    return result
  }

});