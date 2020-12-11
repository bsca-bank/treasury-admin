from dal import autocomplete
#
from django.db.models import Q
#
#from .forms import SendEmailForm


# SendUserEmails view class
# class SendUserEmails():
#     template_name = 'custom/send_email.html'
#     form_class = SendEmailForm
#     success_url = reverse_lazy('admin:users_user_changelist')

#     def form_valid(self, form):
#         users = form.cleaned_data['users']
#         subject = form.cleaned_data['subject']
#         message = form.cleaned_data['message']
#         email_users.delay(users, subject, message)
#         user_message = '{0} users emailed successfully!'.format(form.cleaned_data['users'].count())
#         messages.success(self.request, user_message)
#         return super(SendUserEmails, self).form_valid(form)