import graphene
from accounts.models import Authority, InvitationCode

from accounts.schema.types import (
    AdminInvitationCodeCreateResult,
    AdminInvitationCodeUpdateResult,
    AdminInvitationCodeUpdateProblem,
    AdminInvitationCodeCreateProblem,
)
from accounts.schema.utils import isDupliate, isNotEmpty
from common.types import AdminFieldValidationProblem


class AdminInvitationCodeCreateMutation(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)
        authority_id = graphene.Int(required=True)
        from_date = graphene.DateTime(required=True)
        through_date = graphene.DateTime(required=True)
        inherits = graphene.List(graphene.Int)

    result = graphene.Field(AdminInvitationCodeCreateResult)

    @staticmethod
    def mutate(root, info, code, authority_id, from_date, through_date, inherits):
        problems = []
        if codeProblem := isNotEmpty("code", "Code must not be empty"):
            problems.append(codeProblem)

        if InvitationCode.objects.filter(code=code).exists():
            problems.append(
                AdminFieldValidationProblem(name="code", message="duplicate code")
            )

        if len(problems) > 0:
            return AdminInvitationCodeCreateMutation(
                result=AdminInvitationCodeCreateProblem(fields=problems)
            )
        authority = info.context.user.authorityuser.authority
        if authority_id != 0:
            authority = Authority.objects.get(pk=authority_id)

        invitationCode = InvitationCode.objects.create(
            code=code,
            authority=authority,
            from_date=from_date,
            through_date=through_date,
        )
        return AdminInvitationCodeCreateMutation(result=invitationCode)


class AdminInvitationCodeUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        code = graphene.String(required=True)
        from_date = graphene.DateTime(required=None)
        through_date = graphene.DateTime(required=None)

    result = graphene.Field(AdminInvitationCodeUpdateResult)

    @staticmethod
    def mutate(root, info, id, code, from_date, through_date):
        try:
            invitationCode = InvitationCode.objects.get(pk=id)
        except InvitationCode.DoesNotExist:
            return AdminInvitationCodeUpdateMutation(
                result=AdminInvitationCodeUpdateProblem(
                    fields=[], message="Object not found"
                )
            )

        problems = []
        if invitationCode.code != code:
            if duplicateProblem := isDupliate("code", code, InvitationCode):
                problems.append(duplicateProblem)

        if codeProblem := isNotEmpty("code", "Code must not be empty"):
            problems.append(codeProblem)

        if len(problems) > 0:
            return AdminInvitationCodeUpdateMutation(
                result=AdminInvitationCodeUpdateProblem(fields=problems)
            )

        invitationCode.code = code
        if from_date != None:
            invitationCode.from_date = from_date
        if through_date != None:
            invitationCode.through_date = through_date

        invitationCode.save()

        return {"result": invitationCode}
