from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from src.accounting import views as acc
from src.api.v1.jwt import MyTokenObtainPairView
from src.organization import views as organization
from src.user import views as user
from src.course import views as course
from src.employee import views as emp

router = DefaultRouter()

# organization
router.register("organizations", organization.OrganizationViewSet, "organization")

# User
router.register("users", user.UserViewSet, "user")

# GL
# router.register("account-groups", acc.AccountGroupViewSet, "account-group")
router.register("accounts", acc.AccountViewSet, "accounts")

# Course
router.register("course", course.CourseViewSet) 
router.register("subject", course.SubjectViewSet) 
router.register("section", course.SectionViewSet) 
router.register("attendance/student", course.AttendanceStudentViewSet) 
router.register("attendance/teacher", course.AttendanceTeacherViewSet)

# employee
router.register('employee',emp.EmployeeViewSet),
router.register('employee/leave', emp.LeaveViewSet),
router.register('employee/legalinfo', emp.LegalInfoViewSet)

# router.register("journal-entries", acc.JournalViewSet, "journal-entry")
# router.register("transactions", acc.TransactionViewSet, "transaction")
# router.register("journal-report", acc.JournalEntryReport, "journal-report")

# AR
# router.register("invoice-entries", acc.InvoiceViewSet, "invoice-entry")
# router.register("invoice-report", acc.InvoiceReport, "invoice-report")
#
# router.register("collection-entries", acc.CollectionEntryViewSet, "collection-entry")
# router.register("payment-report", acc.PaymentReport, "payment-report")
#
# router.register("due-invoices", acc.DueInvoiceView, "due-invoice-entry")
#
# router.register("credit-note-entries", acc.CreditNoteEntryViewSet, "credit-note")

# router.register('aged-receivable', acc.AgedReceivableView, base_name='aged-receivable')

# AP
# router.register("billing-entries", acc.BillingEntryViewSet, "billing-entry")
#
# router.register("payment-entries", acc.PaymentViewSet, "payment-entry")
#
# router.register("due-billings", acc.DueBillingView, "due-billing-entry")
#
# router.register("debit-note-entries", acc.DebitNoteEntryViewSet, "debit-note-entry")
#
# router.register("aged-payable", acc.AgedPayableView, "aged-payable")


urlpatterns = [
    # path(
    #     "income-statement/",
    #     acc.IncomeStatementView.as_view({"get": "list"}),
    #     name="income-statement",
    # ),
    # path(
    #     "balance-sheet/",
    #     acc.BalanceSheetView.as_view({"get": "list"}),
    #     name="balance-sheet",
    # ),
    # path(
    #     "trial-balance/",
    #     acc.TrialBalanceView.as_view({"get": "list"}),
    #     name="trial-balance",
    # ),
    # path(
    #     "aged-payable/",
    #     acc.AgedPayableView.as_view({"get": "list"}),
    #     name="aged-payable",
    # ),
    # path(
    #     "aged-receivable/",
    #     acc.AgedReceivableView.as_view({"get": "list"}),
    #     name="aged-receivable",
    # ),
    # path(
    #     "ledger/<int:pk>/",
    #     acc.LedgerViewSet.as_view({"get": "retrieve"}),
    #     name="ledger",
    # ),
    # path(
    #     "cash-flow-statement/",
    #     acc.CashFlowView.as_view({"get": "list"}),
    #     name="cash-flow-statement",
    # ),
    # path(
    #     "dashboard-accounting/",
    #     acc.DashBoardView.as_view({"get": "list"}),
    #     name="dashboard-accounting",
    # ),
    # query_params: payment_id=x for credit/debit voucher, journal_id=x for journal voucher
    # path("get-voucher/", acc.VoucherView.as_view({"get": "list"}), name="get-voucher"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
