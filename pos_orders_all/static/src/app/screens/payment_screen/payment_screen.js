/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ConnectionLostError } from "@web/core/network/rpc_service";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {

	setup() {
		super.setup()
        this.pos = usePos();
        if(this.pos.config.auto_check_invoice){
            this.currentOrder.set_to_invoice(true);
        }
	},

    // async _finalizeValidation() {
    //     if (this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) {
    //         this.hardwareProxy.openCashbox();
    //     }

    //     this.currentOrder.date_order = luxon.DateTime.now();
    //     for (const line of this.paymentLines) {
    //         if (!line.amount === 0) {
    //             this.currentOrder.remove_paymentline(line);
    //         }
    //     }
    //     this.currentOrder.finalized = true;

    //     // 1. Save order to server.
    //     this.env.services.ui.block();
    //     const syncOrderResult = await this.pos.push_single_order(this.currentOrder);
    //     this.env.services.ui.unblock();

    //     let credit_note = this.pos.config.credit_note;
    //     let total =  this.currentOrder.get_total_with_tax();

    //     if (syncOrderResult instanceof ConnectionLostError) {
    //         this.pos.showScreen(this.nextScreen);
    //         return;
    //     } else if (!syncOrderResult) {
    //         return;
    //     }

    //     try {
    //         // 2. Invoice.
    //         if (this.shouldDownloadInvoice() && this.currentOrder.is_to_invoice()) {
    //             if (syncOrderResult.length) {
    //                 console.log("total=========",total)
    //                 console.log("credit_note=========",credit_note)
    //                 if((total >= 0) || (total < 0 && credit_note != "not_create_note")){
    //                     console.log("syncOrderResult =====if======",syncOrderResult)
    //                     await this.report.doAction("account.account_invoices", [
    //                         syncOrderResult[0].account_move,
    //                     ]);
    //                 }
    //                 else {
    //                     const syncOrderResult = await this.pos.push_single_order(this.currentOrder);
    //                     console.log("syncOrderResult=====else====",syncOrderResult)
    //                 }
    //             }else {
    //                 throw { code: 401, message: 'Backend Invoice', data: { order: this.currentOrder } };
    //             }                
    //         } else {
    //             const syncOrderResult = await this.pos.push_single_order(this.currentOrder);
    //         }
    //     } catch (error) {
    //         if (error instanceof ConnectionLostError) {
    //             Promise.reject(error);
    //             return error;
    //         } else {
    //             throw error;
    //         }
    //     }

    //     // 3. Post process.
    //     if (
    //         syncOrderResult &&
    //         syncOrderResult.length > 0 &&
    //         this.currentOrder.wait_for_push_order()
    //     ) {
    //         await this.postPushOrderResolve(syncOrderResult.map((res) => res.id));
    //     }

    //     await this.afterOrderValidation(!!syncOrderResult && syncOrderResult.length > 0);
    // },
});