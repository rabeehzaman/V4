/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        if (this.pos.config.pw_auto_invoice) {
            this.currentOrder.set_to_invoice(true);
        }
    },
    shouldDownloadInvoice() {
        return !this.pos.config.pw_stop_invoice_pdf;
    }
});
