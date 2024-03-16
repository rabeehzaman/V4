    /** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { onMounted, useRef, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";


// IMPROVEMENT: This code is very similar to TextInputPopup.
//      Combining them would reduce the code.
export class MultiUOMPopup extends AbstractAwaitablePopup {
    static template = "bi_pos_multi_uom.MultiUOMPopup";
    static defaultProps = {
        confirmText: _t("Confirm"),
        cancelText: _t("Cancel"),
        title: "Pos Multi UOM",
        body: "",
    };

    /**
     * @param {Object} props
     * @param {string} props.startingValue
     */
    setup() {
        super.setup();
        this.pos=usePos();
        this.state = useState({ inputValue: this.props.startingValue });
        this.inputRef = useRef("input");
        this.popup = useService("popup");
    }

    selectItem(itemId, item_sale_price, item_label, selected_orderline) {
        if (this.pos.get_order().get_orderlines().length > 1){
            for(var line of this.pos.get_order().get_orderlines()){
                if(line.get_product().id == selected_orderline.get_product().id){
                    if(line.uom_id == itemId && line.price == item_sale_price){
                        if(line.price_manually_set == true){
                            var final_qty = line.quantity + selected_orderline.quantity;
                            line.set_quantity(final_qty);
                            this.pos.get_order().remove_orderline(selected_orderline);
                        }
                        this.confirm();
                    }
                }
            }
        }
        selected_orderline.price_type = "manual";
        selected_orderline.set_unit_price(item_sale_price);
        selected_orderline.set_custom_uom_id(itemId);
        this.confirm();
    }
    
    
}
