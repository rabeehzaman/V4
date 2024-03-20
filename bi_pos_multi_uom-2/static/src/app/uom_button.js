/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { MultiUOMPopup } from "@bi_pos_multi_uom/app/uom_popup";

export class UOMButton extends Component {
    static template = "bi_pos_multi_uom.UOMButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
    }
    get filter_uom(){
        var list = []
        var currentOrder = this.pos.get_order();
        var selected_line = currentOrder.get_selected_orderline().product.product_tmpl_id;
        var selected_orderline = currentOrder.get_selected_orderline();
        if(this.env.services.pos.point_of_sale_uom){
            for(var uom_id of this.env.services.pos.point_of_sale_uom){
                if(selected_line == uom_id.product_uom_line_id[0]){
                    list.push({
                        id: uom_id.unit_of_measure_id[0],
                        label : uom_id.unit_of_measure_id[1],
                        sale_price : uom_id.sale_price,
                        symbol: this.env.services.pos.currency.symbol,
                        selected_orderline : selected_orderline,
                    });
                }
            }
        }
        return list;
    }
    async onClick() {

        if(this.pos.get_order().get_selected_orderline()){
            if(this.pos.get_order().get_selected_orderline().product.point_of_sale_uom){
                if(this.pos.get_order().get_selected_orderline().product.product_uom_ids.length > 0){
                    const { confirmed } = await this.popup.add(MultiUOMPopup, {
                        title: _t("Product Multi UOM"),
                        list: this.filter_uom,
                    });
                } else {
                    alert('There Is No Another UOM In This Product.');
                    return;
                }
            } else {
                alert('There Is No UOM');
                return;
            }
        } else {
            alert('Add Product First.');
            return;
        }
    }
}

ProductScreen.addControlButton({
    component: UOMButton,
    condition: function() {
            return this.env.services.pos.config.product_multi_uom;
        },
});
