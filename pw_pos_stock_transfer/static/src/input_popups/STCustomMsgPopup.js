/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { onMounted } from "@odoo/owl";

export class STCustomMsgPopup extends AbstractAwaitablePopup {
    static template = "pw_pos_stock_transfer.STCustomMsgPopup";
    static defaultProps = {
        confirmText: _t("Ok"),
        title: _t("Error"),
        cancelKey: false,
    };

    setup() {
        super.setup();
    }
}
