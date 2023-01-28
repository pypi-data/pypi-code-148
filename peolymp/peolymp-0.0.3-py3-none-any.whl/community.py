from eolymp.community import community_pb2, member_pb2
from eolymp.community.community_http import CommunityClient
from eolymp.wellknown import expression_pb2

from peolymp.abstract import AbstractAPI
from peolymp.utils import get_many


class CommunityAPI(AbstractAPI):
    def __init__(self, **kwargs):
        super(CommunityAPI, self).__init__(**kwargs)
        self.client = CommunityClient(self.http_client, url=self.get_url())

    def get_member(self, member_id):
        return self.client.DescribeMember(community_pb2.DescribeMemberInput(member_id=member_id))

    def get_members(self):
        def get_members(offset, size):
            return self.client.ListMembers(request=community_pb2.ListMembersInput(offset=offset, size=size))

        return get_many(get_members)

    def describe_member(self, member_id):
        return self.client.DescribeMember(community_pb2.DescribeMemberInput(member_id=member_id)).member

    def delete_member(self, member_id):
        return self.client.RemoveMember(community_pb2.RemoveMemberInput(member_id=member_id))

    def delete_all_members(self):
        for member in self.get_members():
            self.delete_member(member.id)

    def make_members_incomplete(self):
        members = self.get_members()
        c = 0
        n = len(members)
        for member in members:
            c += 1
            m = member_pb2.Member(registered=False)
            member.registered = False
            if member.status == 2:
                continue
            print(member)
            print(self.client.UpdateMember(
                community_pb2.UpdateMemberInput(patch=[community_pb2.UpdateMemberInput.REGISTERED], member_id=member.id,
                                                member=m)))

            print((c * 100) // n)

    def find_member(self, user_id):
        member_exp = expression_pb2.ExpressionID(value=user_id)
        setattr(member_exp, 'is', 1)
        member_filter = community_pb2.ListMembersInput.Filter(user_id=[member_exp])
        m = self.client.ListMembers(community_pb2.ListMembersInput(filters=member_filter))
        if m.total == 1:
            return m.items[0]
        return None

    def create_manual_member(self, name, username, password, string_values=[], number_values=[], registered=False,
                             out_of_competition=False):
        identity = member_pb2.Member.Identity(email="fake+" + username + "@eolymp.com",
                                              issuer="https://api.eolymp.com/spaces/" + self.space_id,
                                              nickname=username, password=password)
        values = [member_pb2.Member.Value(attribute_key=pair[0], value_string=pair[1]) for pair in string_values] + \
                 [member_pb2.Member.Value(attribute_key=pair[0], value_number=pair[1]) for pair in number_values]
        member = member_pb2.Member(name=name, registered=registered, values=values, staffed=False,
                                   out_of_competition=out_of_competition, identities=[identity])
        result = self.client.AddMember(community_pb2.AddMemberInput(member=member))
        print(result)
        return result.member_id

    def create_manual_member_oi(self, name, username, password, grade, region, registered=False,
                                out_of_competition=False):
        return self.create_manual_member(name, username, password, string_values=[('region', region), ('name', name)],
                                         number_values=[('grade', int(grade))], registered=registered,
                                         out_of_competition=out_of_competition)

    def change_name(self, member_id, name):
        self.client.UpdateMember(community_pb2.UpdateMemberInput(patch=[community_pb2.UpdateMemberInput.NAME],
                                                                 member_id=member_id,
                                                                 member=member_pb2.Member(name=name)))

    def update_identity(self, member_id, identity_id, identity):
        self.client.UpdateMemberIdentity(
            community_pb2.UpdateMemberIdentityInput(member_id=member_id, identity_id=identity_id, identity=identity))
