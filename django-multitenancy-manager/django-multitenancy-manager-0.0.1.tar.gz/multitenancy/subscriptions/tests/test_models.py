import unittest


from multitenancy.subscriptions.models import Plan, ProductType, Subscription

class TestPlan(unittest.TestCase):
    
    def test_add_feature(self):
        plan = Plan.objects.create(name="basic")
        plan.add_feature("Free domain")

        self.assertEquals(plan.pk,1)
        
        
        