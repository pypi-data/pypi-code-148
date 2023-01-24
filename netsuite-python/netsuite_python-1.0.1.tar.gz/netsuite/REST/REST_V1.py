from netsuite_python.netsuite.REST.V1 import (
    AccountService, AffiliateService, AppointmentService, CampaignService, CompanyService,
    ContactService, EmailService, FileService, LocaleService, MerchantService, NoteService, OpportunityService,
    OrderService, ProductService, SettingService, SubscriptionService, TagService, TaskService, TransactionService,
    UserService)


class REST_V1:
    def __init__(self, netsuite):
        self.netsuite = netsuite
        self.AccountService = AccountService(netsuite)
        self.AffiliateService = AffiliateService(netsuite)
        self.AppointmentService = AppointmentService(netsuite)
        self.CampaignService = CampaignService(netsuite)
        self.CompanyService = CompanyService(netsuite)
        self.ContactService = ContactService(netsuite)
        self.EmailService = EmailService(netsuite)
        self.FileService = FileService(netsuite)
        self.LocaleService = LocaleService(netsuite)
        self.MerchantService = MerchantService(netsuite)
        self.NoteService = NoteService(netsuite)
        self.OpportunityService = OpportunityService(netsuite)
        self.OrderService = OrderService(netsuite)
        self.ProductService = ProductService(netsuite)
        self.SettingService = SettingService(netsuite)
        self.SubscriptionService = SubscriptionService(netsuite)
        self.TagService = TagService(netsuite)
        self.TaskService = TaskService(netsuite)
        self.TransactionService = TransactionService(netsuite)
        self.UserService = UserService(netsuite)

    def test_connection(self):
        return self.SettingService.get_application_status()
