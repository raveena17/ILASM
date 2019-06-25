import sys

from django.conf import settings
from datetime import datetime

from project_management.alert.models import *
from project_management.projectbudget.models import *
from project_management.Utility import EmailWithCC

ERROR_MESSAGE = 'ERROR : %s \nLINE NUMBER : %s'


class TimerAlert:
    def client_document(self):
        '''
        Client document timer alert
        '''
        try:
            logging.info('Client Document Start : ')
            flag = False
            alert_configuration = AlertConfiguration.objects.get(
                pk='alertconfig2')
            if(alert_configuration.is_lock == False):
                return "Inactive"
            oi_list = OI.objects.complex_filter(
                {'is_active': True, 'record_status': 'RS4'})
            oi_list = oi_list.exclude(
                id__in=OIRequest.objects.exclude(
                    oi_type='OITYPE1').values('oi_number'))
            for each_oi in oi_list:
                status_tracker = ClientAgreementStatusTracker.objects.complex_filter(
                    {'oi': each_oi, 'customer_signed_available': 'no'})
                for each_status_tracker in status_tracker:
                    flag = False
                    total_to_email_list, subject_content, body_content, total_cc_email_list = self.data_formation(
                        alert_configuration, each_status_tracker)
                    if len(total_to_email_list) > 0:
                        if(each_oi.crm_name is not None and each_oi.crm_name.email is not None):
                            total_to_email_list.append(each_oi.crm_name.email)
                        if(each_oi.revenue_booked_region.head is not None and each_oi.revenue_booked_region.head.email is not None):
                            total_to_email_list.append(
                                each_oi.revenue_booked_region.head.email)
                        alerttime_details = AlertTime.objects.filter(
                            alert=alert_configuration.pk).filter(
                            record_id=each_status_tracker.pk)
                        if len(alerttime_details) > 0:
                            last_alert_with_days = alerttime_details[0].raised_on + relativedelta(
                                days=alert_configuration.frequency)
                            if date.today() >= last_alert_with_days:
                                alerttime_details.update(
                                    raised_on=date.today())
                                flag = True
                        else:
                            alert_time = AlertTime(
                                alert=alert_configuration,
                                record_id=each_status_tracker.pk,
                                raised_on=date.today())
                            alert_time.save()
                            flag = True
                        if flag:
                            alert_transaction = AlertTransaction(
                                alert=alert_configuration,
                                record_id=each_status_tracker.oi.pk,
                                to_id=total_to_email_list,
                                cc_id=total_cc_email_list,
                                body=body_content,
                                subject=subject_content)
                            alert_transaction.save()
                            if(alert_configuration.is_email):
                                Email().send_email(subject_content, body_content, total_to_email_list,
                                                   settings.EMAIL_CONTENT_TYPE, '', '', total_cc_email_list)
        except BaseException:
            errMessage = ERROR_MESSAGE % (
                sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
            logging.info('Client Document Error : ' + errMessage)
        else:
            logging.info('Client Document End : ')

    def valid_document(self):
        '''
        Valid document timer alert
        '''
        try:
            logging.info('Valid Document Start : ')
            flag = False
            alert_configuration = AlertConfiguration.objects.get(
                pk='alertconfig5')
            if(alert_configuration.is_lock == False):
                return "Inactive"
            oi_list = OI.objects.complex_filter(
                {'is_active': True, 'record_status': 'RS4'})
            oi_list = oi_list.exclude(
                id__in=OIRequest.objects.exclude(
                    oi_type='OITYPE1').values('oi_number'))
            for each_oi in oi_list:
                status_tracker = ClientAgreementStatusTracker.objects.complex_filter({
                                                                                     'oi': each_oi})
                for each_status_tracker in status_tracker:
                    flag = False
                    total_to_email_list, subject_content, body_content, total_cc_email_list = self.data_formation(
                        alert_configuration, each_status_tracker)
                    if len(total_to_email_list) > 0:
                        if(each_oi.crm_name is not None and each_oi.crm_name.email is not None):
                            total_to_email_list.append(each_oi.crm_name.email)
                        if(each_oi.revenue_booked_region.head is not None and each_oi.revenue_booked_region.head.email is not None):
                            total_to_email_list.append(
                                each_oi.revenue_booked_region.head.email)
                        alerttime_details = AlertTime.objects.filter(
                            alert=alert_configuration.pk).filter(
                            record_id=each_status_tracker.pk)
                        if len(alerttime_details) > 0:
                            alert_check = each_status_tracker.valid_till + \
                                relativedelta(days=alert_configuration.days)
                            if (alert_check <= date.today()):
                                last_alert_with_days = alerttime_details[0].raised_on + relativedelta(
                                    days=alert_configuration.frequency)
                                if date.today() >= last_alert_with_days:
                                    alerttime_details.update(
                                        raised_on=date.today())
                                    flag = True
                        else:
                            last_alert_with_days = each_status_tracker.valid_till + \
                                relativedelta(days=alert_configuration.days)
                            if date.today() == last_alert_with_days:
                                alert_time = AlertTime(
                                    alert=alert_configuration,
                                    record_id=each_status_tracker.pk,
                                    raised_on=date.today())
                                alert_time.save()
                                flag = True
                        if flag:
                            alert_transaction = AlertTransaction(
                                alert=alert_configuration,
                                record_id=each_status_tracker.oi.pk,
                                to_id=total_to_email_list,
                                cc_id=total_cc_email_list,
                                body=body_content,
                                subject=subject_content)
                            alert_transaction.save()
                            if(alert_configuration.is_email):
                                Email().send_email(subject_content, body_content, total_to_email_list,
                                                   settings.EMAIL_CONTENT_TYPE, '', '', total_cc_email_list)
        except BaseException:
            errMessage = ERROR_MESSAGE % (
                sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
            logging.info('Valid Till Date Error : ' + errMessage)
        else:
            logging.info('Valid Document End : ')

    def hardcopy_recived(self):
        '''
        Hardcopy received timer alert
        '''
        try:
            logging.info('Hardcopy Received Start : ')
            flag = False
            alert_configuration = AlertConfiguration.objects.get(
                pk='alertconfig6')
            if(alert_configuration.is_lock == False):
                return "Inactive"
            oi_list = OI.objects.complex_filter(
                {'is_active': True, 'record_status': 'RS4'})
            oi_list = oi_list.exclude(
                id__in=OIRequest.objects.exclude(
                    oi_type='OITYPE1').values('oi_number'))
            for each_oi in oi_list:
                status_tracker = ClientAgreementStatusTracker.objects.complex_filter(
                    {'oi': each_oi, 'hard_copy_received_from_customer': 'yes', 'hard_copy_submitted_to_finance': 'no'})
                for each_status_tracker in status_tracker:
                    flag = False
                    total_to_email_list, subject_content, body_content, total_cc_email_list = self.data_formation(
                        alert_configuration, each_status_tracker)
                    if len(total_to_email_list) > 0:
                        alerttime_details = AlertTime.objects.filter(
                            alert=alert_configuration.pk).filter(
                            record_id=each_status_tracker.pk)
                        if len(alerttime_details) > 0:
                            last_alert_with_days = alerttime_details[0].raised_on + relativedelta(
                                days=alert_configuration.frequency)
                            if date.today() >= last_alert_with_days:
                                alerttime_details.update(
                                    raised_on=date.today())
                                flag = True
                        else:
                            alert_time = AlertTime(
                                alert=alert_configuration,
                                record_id=each_status_tracker.pk,
                                raised_on=date.today())
                            alert_time.save()
                            flag = True
                        if flag:
                            alert_transaction = AlertTransaction(
                                alert=alert_configuration,
                                record_id=each_status_tracker.oi.pk,
                                to_id=total_to_email_list,
                                cc_id=total_cc_email_list,
                                body=body_content,
                                subject=subject_content)
                            alert_transaction.save()
                            if(alert_configuration.is_email):
                                Email().send_email(subject_content, body_content, total_to_email_list,
                                                   settings.EMAIL_CONTENT_TYPE, '', '', total_cc_email_list)
        except BaseException:
            errMessage = ERROR_MESSAGE % (
                sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
            logging.info('Hard Copy Received Error : ' + errMessage)
        else:
            logging.info('Hardcopy Received End : ')

    def valid_internal_date(self):
        '''
        Internal validity timer alert
        '''
        try:
            logging.info('Internal Validity Start : ')
            flag = False
            alert_configuration = AlertConfiguration.objects.get(
                pk='alertconfig13')
            if(alert_configuration.is_lock == False):
                return "Inactive"
            oi_list = OI.objects.complex_filter(
                {'is_active': True, 'record_status': 'RS4', 'approval_type': 'APPTYPE4'})
            oi_list = oi_list.exclude(
                id__in=OIRequest.objects.exclude(
                    oi_type='OITYPE1').values('oi_number'))
            for each_status_tracker in oi_list:
                flag = False
                total_to_email_list, subject_content, body_content, total_cc_email_list = self.data_formation(
                    alert_configuration, each_status_tracker)
                if len(total_to_email_list) > 0:
                    if(each_status_tracker.crm_name is not None and each_status_tracker.crm_name.email is not None):
                        total_to_email_list.append(
                            each_status_tracker.crm_name.email)
                    if(each_status_tracker.revenue_booked_region.head is not None and each_status_tracker.revenue_booked_region.head.email is not None):
                        total_to_email_list.append(
                            each_status_tracker.revenue_booked_region.head.email)
                    alerttime_details = AlertTime.objects.filter(
                        alert=alert_configuration.pk).filter(
                        record_id=each_status_tracker.pk)
                    if(each_status_tracker.internal_approval_validity_date is None):
                        continue

                    if len(alerttime_details) > 0:
                        alert_check = each_status_tracker.internal_approval_validity_date + \
                            relativedelta(days=alert_configuration.days)
                        if (alert_check <= date.today()):
                            last_alert_with_days = alerttime_details[0].raised_on + relativedelta(
                                days=alert_configuration.frequency)
                            if date.today() >= last_alert_with_days:
                                alerttime_details.update(
                                    raised_on=date.today())
                                flag = True
                    else:
                        last_alert_with_days = each_status_tracker.internal_approval_validity_date + \
                            relativedelta(days=alert_configuration.days)
                        if date.today() == last_alert_with_days:
                            alert_time = AlertTime(
                                alert=alert_configuration,
                                record_id=each_status_tracker.pk,
                                raised_on=date.today())
                            alert_time.save()
                            flag = True
                    if flag:
                        alert_transaction = AlertTransaction(
                            alert=alert_configuration,
                            record_id=each_status_tracker.pk,
                            to_id=total_to_email_list,
                            cc_id=total_cc_email_list,
                            body=body_content,
                            subject=subject_content)
                        alert_transaction.save()
                        if(alert_configuration.is_email):
                            Email().send_email(subject_content, body_content, total_to_email_list,
                                               settings.EMAIL_CONTENT_TYPE, '', '', total_cc_email_list)
        except BaseException:
            errMessage = ERROR_MESSAGE % (
                sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
            logging.info('Internal Validity Error : ' + errMessage)
        else:
            logging.info('Internal Approval End : ')

    def data_formation(self, alert_configuration, each_status_tracker):
        '''
        Formation of mail contents
        '''
        allow_practice = False
        allow_bu = False
        if(alert_configuration.pk == 'alertconfig13'):
            bucode_id = each_status_tracker.oirequestnumber.bu_code.id
        else:
            bucode_id = each_status_tracker.oi.oirequestnumber.bu_code.id
        bu_code = BUCode.objects.filter(id=bucode_id)
        if len(bu_code) > 0:
            allow_bu = True if(
                bu_code[0].alert_option == 'BU' or bu_code[0].alert_option == 'All') else False
            allow_practice = True if(
                bu_code[0].alert_option == 'Practice' or bu_code[0].alert_option == 'All') else False

        total_to_email_list = []
        total_cc_email_list = []
        subject_fields_lsit = []
        body_fields_list = []
        subject_fields = alert_configuration.subject_fields.split(',')
        for each_subfield in subject_fields:
            subject_fields_lsit.append(
                eval(
                    'each_status_tracker.' +
                    str(each_subfield)))
        body_fields = alert_configuration.body_fields.split(',')
        for each_bodyfield in body_fields:
            body_fields_list.append(
                eval(
                    'each_status_tracker.' +
                    str(each_bodyfield)))
        subject_content = alert_configuration.subject % tuple(
            subject_fields_lsit)
        body_content = alert_configuration.body % tuple(body_fields_list)
        to_email = alert_configuration.toemail.values()
        for each_email in to_email:
            total_to_email_list.append(each_email.get('email'))
        to_cc = alert_configuration.cc.values()
        for each_cc in to_cc:
            total_cc_email_list.append(each_cc.get('email'))
        to_bcc = alert_configuration.bcc.values()
        for each_bcc in to_bcc:
            total_cc_email_list.append(each_bcc.get('email'))
        roles = alert_configuration.role.values()
        for each_role in roles:
            role_resources = RoleResource.objects.filter(
                role=each_role.get('id')).filter(is_active=True)
            for each_role in role_resources:
                resource_list = each_role.resource.values()
                for each_resource in resource_list:
                    total_to_email_list.append(each_resource.get('email'))
        if allow_practice:
            for each_prac in alert_configuration.practice_email_type.split(
                    ','):
                if each_prac == 'All':
                    resources = Resources.objects.filter(is_active=True)
                    for each_user in resources:
                        resource_user_list = each_user.practice.filter(
                            pk=each_status_tracker.oirequestnumber.practice_code.id)
                        if len(resource_user_list) > 0:
                            user_obj = User.objects.get(
                                pk=each_user.auth_user.id)
                            total_cc_email_list.append(user_obj.email)
                else:
                    if(alert_configuration.pk == 'alertconfig13'):
                        practice_codes = PracticeCode.objects.filter(is_active=True).filter(
                            pk=each_status_tracker.oirequestnumber.practice_code.id)
                    else:
                        practice_codes = PracticeCode.objects.filter(is_active=True).filter(
                            pk=each_status_tracker.oi.oirequestnumber.practice_code.id)
                    for each_practice in practice_codes:
                        if each_prac == 'CT':
                            if(each_practice.team_email is not None):
                                for each_prac_email in each_practice.team_email.split(
                                        ','):
                                    total_cc_email_list.append(each_prac_email)
                        if each_prac == 'RH':
                            if(each_practice.reporting is not None and each_practice.reporting.email is not None):
                                total_cc_email_list.append(
                                    each_practice.reporting.email)

        if allow_bu:
            for each_bu in alert_configuration.bu_email_type.split(','):
                if each_bu == 'All':
                    resources = Resources.objects.filter(is_active=True)
                    for each_user in resources:
                        resource_user_list = each_user.bu_code.filter(
                            pk=each_status_tracker.oirequestnumber.bu_code.id)
                        if len(resource_user_list) > 0:
                            user_obj = User.objects.get(
                                pk=each_user.auth_user.id)
                            total_cc_email_list.append(user_obj.email)
                else:
                    if(alert_configuration.pk == 'alertconfig13'):
                        bu_codes = BUCode.objects.filter(is_active=True).filter(
                            pk=each_status_tracker.oirequestnumber.bu_code.id)
                    else:
                        bu_codes = BUCode.objects.filter(is_active=True).filter(
                            pk=each_status_tracker.oi.oirequestnumber.bu_code.id)
                    for each_bucode in bu_codes:
                        if each_bu == 'CT':
                            if(each_bucode.core_team is not None):
                                for each_bu_email in each_bucode.core_team.split(
                                        ','):
                                    total_cc_email_list.append(each_bu_email)
                        if each_bu == 'RH':
                            if(each_bucode.reporting is not None and each_bucode.reporting.email is not None):
                                total_cc_email_list.append(
                                    each_bucode.reporting.email)

        other_alerts = AlertOthers.objects.filter(
            alertconfiguration=alert_configuration)
        if len(other_alerts) > 0:
            for each_alert in other_alerts:
                for each_dep in each_alert.dept_email_type.split(','):
                    if each_dep == 'All':
                        resources = Resources.objects.complex_filter(
                            {'department': each_alert.department, 'is_active': True})
                        for each_user in resources:
                            user_obj = User.objects.get(
                                pk=each_user.auth_user.id)
                            total_to_email_list.append(user_obj.email)
                    else:
                        departments = Department.objects.filter(
                            is_active=True).filter(
                            pk=each_alert.department.id)
                        for each_department in departments:
                            if each_dep == 'CT':
                                if(each_department.team_email is not None):
                                    for each_dep_email in each_department.team_email.split(
                                            ','):
                                        total_to_email_list.append(
                                            each_dep_email)
                            if each_dep == 'RH':
                                if(each_department.head is not None and each_department.head.email is not None):
                                    total_to_email_list.append(
                                        each_department.head.email)

        total_to_email_list = filter(None, total_to_email_list)
        total_cc_email_list = filter(None, total_cc_email_list)
        return total_to_email_list, subject_content, body_content, total_cc_email_list
