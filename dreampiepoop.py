import datetime
sys.path.append('/home/jlmarks/ts/')
import treadstone
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
tcon=treadstone.ISServer(treadstone.settings['appname'], treadstone.settings['apikey'])
p=tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
p
import datetime
for eachthing in p:
    print eachthing['DueDate'].value
ed = datetime.datetime(2015,03,03)
treadstone.deleteInvoicesForSubscriptions(tcon, 131, ed)
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
len(recurringOrder)
recurringOrder=tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": True})
recurringOrder
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
recurringOrder
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 0, 'BillingAmt':123.45, 'EndDate': '2015-02-01','PaidThruDate': '2015-01-01', 'Status': 'Inactive'})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
treadstone.deleteInvoicesForSubscriptions(tcon, 131)



jd1 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1, 'BillingAmt':123.45, 'EndDate': '', 'Status': 'Active'})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
enddate = datetime.datetime(2015,05,05)
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
jd2 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 0, 'EndDate': '2015-05-05', 'Status': 'Inactive'})
treadstone.deleteInvoicesForSubscriptions(tcon, 131, deleteAfter=enddate)
jd3 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
nro = tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})









import uuid
p='a'
p+='e'
p
sys.path.append('/home/jlmarks/ts/')
import treadstone
sys.path.append('/home/jlmarks/ts/')
import treadstone
treadstone.v1()
a
treadstone.settings
p=treadstone.ISServer()
a=fullexport.fullexporter('if188')
a=fullexport.fullexporter('if188')
import os
import sys
import csv
import urllib3
import ssl
import re
import ssl


import threading
import requests
from Queue import Queue

import ISServer_master as ISServer
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()
class tat():
    global pw
    def __init__(self, appname=None):
        self.startingpath = os.path.abspath(os.curdir)
        if not appname:
            self.appname=self.getappname()
        else:
            self.appname = appname
        self.apppath = os.path.join(self.startingpath, self.appname)
        if not os.path.exists(self.apppath):
            os.mkdir(self.apppath)
        os.chdir(self.apppath)
        self.mapping={}
        self.mapping['Contact']=-1
        self.mapping['Affiliate']=-3
        self.mapping['ContactAction']=-5
        self.mapping['Company']=-6
        self.mapping['OrderItem']=-9

        self.menu()
    def menu(self, context="initial"):
        if context is "initial":
            self.baseurl = 'https://' + self.appname + '.infusionsoft.com/'
            self.apikey=self.getapikey()
            self.svr = ISServer.ISServer(self.appname, self.apikey)
            if not os.path.exists(self.apppath):
                os.mkdir(self.apppath)
            os.chdir(self.apppath)
            if not os.path.exists('files'):
                os.mkdir('files')
            os.chdir('files')
            self.usermenu={}
            self.usermenu['downloadAPITables'] = 'apit'
            self.usermenu['play'] = 'play'
            self.usermenu['reports'] = 'rpts'
        # for eachitem in self.usermenu.keys():
        #     print eachitem + ":\t" + self.usermenu[eachitem]
        # thisChoice = raw_input('please make a choice: ').strip(' \n\t')
        thisChoice = 'play'
        if thisChoice == 'apit':
            self.handleAPItables()
        elif thisChoice == 'play':
            self.play()
        elif thisChoice == 'rpts':
            self.downloadAllReports()
        else:
            self.inchandlefiles()
    def handlefiles(self):
        os.chdir(self.startingpath)
        if not os.path.exists('files'):
            os.mkdir('files')
        os.chdir('files')
        allfiles = self.svr.getAllRecords('FileBox')
        for eachfile in allfiles:
            downloadurl = self.baseurl+"Download?Id="+str(eachfile['Id'])
            self.browser.open(downloadurl)
            fileoutpath = os.path.join(self.startingpath, 'files', eachfile['ContactId'], eachfile['FileName'])
            if not os.path.exists(os.path.dirname(fileoutpath)):
                os.makedirs(fileoutpath)
            fout = open(fileoutpath, 'wb')
            fout.write(self.browser.response.content)
            fout.close()
    def inchandleAPItables(self):
        apidata={}
        self.customfields=self.svr.getAllRecords('DataFormField')
        for eachtable in ISServer.tables.keys():
            if eachtable not in ["LeadSourceExpense", "DataFormTab", "GroupAssign", "AffResource", "InvoiceItem", "UserGroup", "CProgram", "ActionSequence", "Template", "LeadSource", "Status", "Campaignee", "DataFormField", "OrderItem", "DataFormGroup", "ProductOptValue", "ContactGroup", "Company", "TicketStage", "ProductCategoryAssign", "ContactGroupAssign"]:
                print "starting " + eachtable
                if eachtable not in self.mapping.keys():
                    self.mapping[eachtable]=99
                fields = ISServer.tables[eachtable] +  ['_'+fld['Name'] for fld in self.customfields if fld['FormId'] is self.mapping[eachtable]]
                self.svr.incrementlyGetRecords(eachtable, interestingData=fields)
                print "done writing " + eachtable
            else:
                print "already completed "+ eachtable
        self.apidata = apidata
    def inchandleAPItable(self, tablename):
        self.customfields=self.svr.getAllRecords('DataFormField')
        if tablename not in self.mapping.keys():
            self.mapping[tablename]=99
        fields = ISServer.tables[tablename] +  ['_'+fld['Name'] for fld in self.customfields if fld['FormId'] is self.mapping[tablename]]
        self.svr.incrementlyGetRecords(tablename, interestingData=fields)
        print "done writing " + tablename
    def inchandlefiles(self):
        os.chdir(self.startingpath)
        self.svr.incgetfiles(self.browser)
    def downloadContact0files(self, numberofmostrecentfilestodownload):
        thesefiles = self.svr.getAllRecords('FileBox', searchCriteria={'ContactId': 0})
        for eachfile in thesefiles[-int(numberofmostrecentfilestodownload):]:
            print "doing " + str(eachfile)
            self.svr.getfile(self.browser, eachfile)
    def play(self):
        print "she's all yours captain!"
    def downloadAReport(self, reportname):
        self.browser.open(self.baseurl + "Reports/exportResults.jsp?reportClass=" + reportname)
        reportForm = [eachform for eachform in self.browser.get_forms() if eachform.action == 'qbExport.jsp']
        if len(reportForm) > 0:
            self.browser.submit_form(reportForm[0], submit=reportForm[0].submit_fields['process'])
            with open(reportname+".csv", 'wb') as outfile:
                outfile.write(self.browser.response.content)
        else:
            print "no " + reportname
    def downloadAllReports(self):
        for reportname in [ "AffiliateActivitySummary", "AffiliateLedger", "AffiliateRedirectActivity", "AffiliateReferral", "AffPayout", "AllOrders", "AllSales", "AllSalesItemized", "ARAgingReport", "CampaigneeBasic", "CampaigneeByDay", "CampaignProductConversion", "ClickThroughPercentage", "ClickThroughPercentageByEmail", "ContactDistributed", "CProgramRevenueSummary", "CreditCard", "CreditsIssued", "CustomerLifetimeValue", "DailyPayments", "DailyReceivables", "DailySalesTotals", "DashboardCampaign", "DashboardEmail", "DashboardLeads", "DashboardOrders", "DashboardUsers", "DigitalProductKey", "EmailBatchSearch", "EmailBroadcastConversionReport", "EmailConversion", "EmailSentSearch", "FailedCharge", "FaxBatchSearch", "FollowUpSequenceConversionReport", "FunnelFlowRecipient", "FunnelFlowRecipientWaiting", "FunnelGoalAchieved", "FunnelQueuedFlowItem", "FunnelUniqueContacts", "GroupAdds", "HabeasDetail", "InvoiceNetIncome", "LeadSourceConversion", "LeadSourceIncome", "LeadSourceROI", "LeadSourceROIByCategory", "MonthlyPayments", "MonthlyReceivables", "MonthlySalesTotals", "MonthlySalesTotalsByProduct", "OptOutSearch", "PaymentsReport", "PieceResponse", "ProductNetIncome", "Receivables", "RevenueForecastReport", "TaskSearch", "VoiceBatchSearch", "VoiceOptOutSearch", "WebformActivitySummary", "WebFormTracking" ]:
            self.downloadAReport(reportname)
    def getFilePath(self):
        return tkFileDialog.askopenfilename()
    def getFolderPath(self):
        return tkFileDialog.askdirectory()
    def getappname(self):
        return raw_input("Please enter appname:").strip('\n \t')
    def getapikey(self):
        global pw
        username = pw['username']
        password = pw['password']
        #Basically:
        #    #Add username and password to your global variables.
        self.browser = RoboBrowser(history=True)
        self.browser.open(self.baseurl)
        logform = self.browser.get_form()
        logform.fields['username'].value = username
        logform.fields['password'].value = password
        self.browser.submit_form(logform)
        self.browser.follow_link(self.browser.get_links()[1])
        self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
        pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
        return pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text
    def handleAPItables(self):
        apidata={}
        self.customfields=self.svr.getAllRecords('DataFormField')
        for eachtable in ISServer.tables.keys():
            print "starting " + eachtable
            if eachtable not in self.mapping.keys():
                self.mapping[eachtable]=99
            fields = ISServer.tables[eachtable] +  ['_'+fld['Name'] for fld in self.customfields if fld['FormId'] is self.mapping[eachtable]]
            apidata[eachtable] =  self.svr.getAllRecords(eachtable, interestingData=fields)
            with open(eachtable+".csv", 'wb') as outfile:
                writer=csv.DictWriter(outfile, fields)
                writer.writeheader()
                writer.writerows(apidata[eachtable])
            print "done writing " + eachtable
        self.apidata = apidata
    def handlewebforms(self):
        # for eachid
        # webformsubmissionpath="https://" + self.appname + ".infusionsoft.com/app/webformSubmission/contactTabDetails?customFormWebResultId=" + str(x)
        pass
    def creditCardsToCSV(self):
        ccs = self.svr.getAllRecords('CreditCard', interestingData=['Id', 'ContactId', "CardType", "Last4", "ExpirationMonth", "ExpirationYear", "Email",  "StartDateMonth", "StartDateYear", "Status"])
        os.chdir(self.startingpath)
        if not os.path.exists('pyDatas'):
            os.mkdir('pyDatas')
        os.chdir('pyDatas')
        with open('ccs.csv', 'wb') as outfile:
            thiswriter = csv.DictWriter(outfile, ccs[0].keys())
            thiswriter.writeheader()
            thiswriter.writerows(ccs)
        print "File written to " + str(os.path.abspath(os.curdir))
        os.chdir(self.startingpath)
    def contactsToCSV(self):
        os.chdir(self.startingpath)
        self.customfields = self.svr.getAllRecords('DataFormField')
        fields = ISServer.tables['Contact'] +  ['_'+fld['Name'] for fld in self.customfields if fld['FormId'] == -1]
        cons = self.svr.getAllRecords('Contact', interestingData = fields)
        if not os.path.exists('pyDatas'):
            os.mkdir('pyDatas')
        os.chdir('pyDatas')
        with open('contacts.csv', 'wb')as outfile:
            thiswriter = csv.DictWriter(outfile, cons[0].keys())
            thiswriter.writeheader()
            thiswriter.writerows(cons)
a=tat()
if188
ab=RoboBrowser(history=True)
import os
import sys
import csv
import urllib3
import ssl
import re
import ssl


import threading
import requests
from Queue import Queue

import ISServer_master as ISServer
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()
ab=RoboBrowser(history=True)
pw['username']
ab.open('https://if188.infusionsoft.com')
lf=ab.get_form()
lf.fields['username']=pw['username']
lf.fields['password']=pw['password']
ab.submit_form(lf)
lf=ab.get_form()
lf.fields['username'].value=pw['username']
lf.fields['password'].value=pw['password']
ab.submit_form(lf)
a=fullexport.fullexporter('if188')
a=fullexport.fullexporter('if188')
a.svr.getAllRecords('RecurringOrder', searchCriteria={'ContactId': 60349})
a.svr.getAllRecords('RecurringOrder', searchCriteria={'ReasonStopped': "37ab5c71-0bdf-43d1-9bde-26054d705213"})
a.svr.getAllRecords('RecurringOrder', searchCriteria={'ReasonStopped': "_37ab5c71-0bdf-43d1-9bde-26054d705213_"})
a.svr.getAllRecords('RecurringOrder', searchCriteria={'ReasonStopped': "_37ab5c71-0bdf-43d1-9bde-26054d705213%"})
sys.path.append('/home/jlmarks/ts/')
import treadstone
treadstone.v2()
import treadstone
sys.path.append('/home/jlmarks/ts/')
import treadstone
treadstone.v2()
sys.path.append('/home/jlmarks/ts/')
import treadstone
treadstone.v2()
global thisconnection
'thisconnection' in globals()
sys.path.append('/home/jlmarks/ts/')
import treadstone
sys.path.append('/home/jlmarks/ts/')
import treadstone
'thisconnection' in globals()
global thisconnection
'thisconnection' in globals()
tcon=treadstone.ISServer(treadstone.settings['appname'], treadstone.settings['apikey'])
thissub = treadstone.findSubByUUIDInReasonStopped("37ab5c71-0bdf-43d1-9bde-26054d705213", tcon)
thissub[0]['Id']
tcon.updateRecord('RecurringOrder', 131, {'AutoCharge': True})
thissub[0]['BillingCycle']
tcon.updateRecord('RecurringOrder', 131, {'BillingCycle': 3})
tcon.updateRecord('RecurringOrder', 131, {'AutoCharge': True})
import treadstone
sys.path.append('/home/jlmarks/ts/')
import treadstone
treadstone.v2()
p=treadstone.thisconnection.getAllRecords('RecurringOrder')
p
len(p)
for eachp in p:
    print eachp['Id']
p=treadstone.thisconnection.getAllRecords('JobRecurringInstance')
p[0]
p[-1]
p=treadstone.thisconnection.getAllRecords('Invoice')
p=treadstone.thisconnection.getAllRecords('Invoice', searchCriteria={'JobId': 131})
p
p=treadstone.thisconnection.getAllRecords('Invoice')
p[1]
p[-1]
import datetime
print p[-1]['DateCreated']
for eachthing in p:
    print p['DateCreated']
for eachthing in p:
    print eachthing['DateCreated']
for eachthing in p:
    print eachthing['DateCreated'], eachthing['Id']
p=treadstone.thisconnection.getAllRecords('Invoice', searchCriteria={'Id': 3411})
p[0]
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'Id': 3411})
p
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
len(p)
p[0]
p[1]
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': datetime.datetime(2015,1,1)})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': datetime.datetime(2015,1,1,0,0,0)})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '1-1-2015'})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '1/1/2015'})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDadte': '1/1/2015'})
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '1/1/2015%'})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '%'})
op
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '1%'})
op
len(op)
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '0%'})
len(op)
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '>=01%'})
len(op)
op=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131,  'DueDate': '2015-03-%'})
op
len(op)
dd
dd=datetime.datetime.now()
op[0]['DateCreated'] > dd
op[0]['DateCreated'] - dd
op[0]['DateCreated'] .value
ee=datetime.datetime(op[0]['DateCreated'])
ee=datetime.datetime(op[0]['DateCreated'].value)
op[0]['DateCreated'] .timetuple
kk=op[0]['DateCreated'] .timetuple()
kk
kk+dd
kk.n_fields
kk.n_sequence_fields
kk.n_unnamed_fields
type(op[0]['DateCreated'] )
op[0]['DateCreated']
print datetime.date(op[0]['DateCreated'])
str(op[0]['DateCreated'])
popoo=datetime.datetime.now()
popoo.strftime('%Z')
popoo.tzname
popoo.tzname()
print popoo.tzname()
sys.path.append('/home/jlmarks/ts/')
import treadstone
p=treadstone.thisconnection.getAllRecords('Invoice', searchCriteria={'JobId': 131})
p[0]
p=treadstone.thisconnection.getAllRecords('Invoice', searchCriteria={'Id': 3411})
p[0]
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'Id': 131})
p
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
p
import datetime
popoo=datetime.datetime.now()
popool = datetime.datetime.now()
popoo > popool
popoo < popool
pp = popoo - popool
pp
p=treadstone.thisconnection.getAllRecords('JobRecurringInstance')
p
len(p)
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
p
p[0]
i=treadstone.thisconnection.getAllRecords('Invoice', searchCriteria={'JobId':3411})
i
p[0]['DueDate'].value
import datetime
sys.path.append('/home/jlmarks/ts/')
import treadstone
p=treadstone.thisconnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
tcon=treadstone.ISServer(treadstone.settings['appname'], treadstone.settings['apikey'])
p=tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
p
import datetime
for eachthing in p:
    print eachthing['DueDate'].value
ed = datetime.datetime(2015,03,03)
treadstone.deleteInvoicesForSubscriptions(tcon, 131, ed)
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
len(recurringOrder)
recurringOrder=tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": True})
recurringOrder
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
recurringOrder
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 0, 'BillingAmt':123.45, 'EndDate': '2015-02-01','PaidThruDate': '2015-01-01', 'Status': 'Inactive'})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
recurringOrder
treadstone.deleteInvoicesForSubscriptions(tcon, 131)
jd1 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1, 'BillingAmt':123.45, 'EndDate': '', 'Status': 'Active'})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
enddate = datetime.datetime(2015,05,05)
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
jd2 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 0, 'EndDate': '2015-05-05', 'Status': 'Inactive'})
treadstone.deleteInvoicesForSubscriptions(tcon, 131, deleteAfter=enddate)
jd3 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
nro = tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
jd1
recurringOrder
jd2
jd3
nro
recurringOrder
jd1 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1, 'BillingAmt':123.45, 'EndDate': '', 'Status': 'Active'})
jd1 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
print tcon.updateRecord('RecurringOrder', 131,{"AutoCharge": 1, 'BillingAmt':123.45, 'EndDate': '', 'Status': 'Active'})
recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
enddate = datetime.datetime(2015,05,05)
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
jd1 = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 131})
print tcon.updateRecord('RecurringOrder', 131,{"NextBillDate": '2015-01-01'})
jd1
jd1 = tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})
jd1
tcon.connection.InvoiceService.updateJobRecurringNextBillDate(treadstone.settings['apikey'], '2015-01-01')
tcon.connection.InvoiceService.updateJobRecurringNextBillDate(treadstone.settings['apikey'], 131,  '2015-01-01')
tcon.connection.InvoiceService.updateJobRecurringNextBillDate(treadstone.settings['apikey'], 131,  datetime.datetime(2015,05,05))
tcon.connection.InvoiceService.updateJobRecurringNextBillDate(treadstone.settings['apikey'], 131,  datetime.datetime(2015,01,01))
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
tcon.connection.InvoiceService.updateJobRecurringNextBillDate(treadstone.settings['apikey'], 131,  datetime.datetime(2015,01,15))
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 131)
treadstone.v1()

sdf
treadstone.v1()
l
pcc='d221f4c2-9b9b-4966-a295-65c13f80288f'
pl=treadstone.findSubByUUIDInReasonStopped(tcon, pcc)
pl[0]
pl=tcon.getAllRecords('RecurringOrder', searchCriteria={'PromoCode': pcc})
pl
jd1 = tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 133})
tcon.updateRecord('RecurringOrder', 133,{"AutoCharge": 1, 'EndDate': '', 'Status': 'Active'})
enddate = datetime.datetime(2015,05,05)
tcon.connection.InvoiceService.createInvoiceForRecurring(treadstone.settings['apikey'], 133)
jd2 = tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 133})
tcon.updateRecord('RecurringOrder', 133,{"AutoCharge": 0, 'EndDate': '2015-05-05', 'Status': 'Inactive'})
treadstone.deleteInvoicesForSubscriptions(tcon, 133, deleteAfter=enddate)
jobsData = apiConnection.getAllRecords('Job', searchCriteria={'JobRecurringId': 133})
jobsData = tcon.getAllRecords('Job', searchCriteria={'JobRecurringId': 133})
jobsData
for eachJob in jobsData:
    duedate = datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
    if  duedate>deleteAfter:
        invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
        print invoiceData
for eachJob in jobsData:
    duedate = datetime.datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
    if  duedate>deleteAfter:
        invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
        print invoiceData
for eachJob in jobsData:
    duedate = datetime.datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
    if  duedate>enddate:
        invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
        print invoiceData
for eachJob in jobsData:
    duedate = datetime.datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
    if  duedate>enddate:
        print "hello!"
        invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
        print invoiceData
    else:
        print "Boo"
for eachJob in jobsData:
    duedate = datetime.datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
    if  duedate>enddate:
        print "hello!"
        invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
        print invoiceData
    else:
        print str(duedate) + " is less than "  + str(enddate)
        print "Boo"




import os
appf = os.path.abspath(os.path.join(os.path.curdir, 'if188'))
appf
os.path.isdir(appf)
appf = os.path.abspath(os.path.join(os.path.curdir, 'flamingahole'))
os.path.isdir(appf)
os.path.isfile(appf)
os.makedirs(appf)
os.path.isfile(appf)
os.path.isdir(appf)
os.path.isdir(appf)
os.path.isfile(appf)
os.path.isfile(appf)
os.makedirs(appf)
a='/home/jlmarks/popopopopopopopo'
os.makedirs(a)
a=fullexport.fullexporter()
if188
a.apikey
tt=a.svr.connection.DataService.query(a.apikey, 'Contact', 1, 0, {}, ['Id'], ['Id'], False)
tt
tt=a.svr.connection.DataService.query(a.apikey, 'Contact', 1, 0, {}, ['Id'], ['Id'], True)
tt
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
import os
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
a.getmaxid('Contact')
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
a.getmaxid('Contact')
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
a.getmaxid('Contact')
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
a.getmaxid('Contact')
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/somecsv.csv', pw['apikey'])
a.getmaxid('Contact')
a.tableSnapshot()
a.tableSnapshot()
import uuid
uuid.uuid4()
pppp=uuid.uuid4()
sys.path.append('/home/jlmarks/ts/')
import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/if188start.csv', pw['apikey'])
a.prepareFile()
sys.path.append('/home/jlmarks/ts/')




import treadstone
a=treadstone.HisSubImp(pw['app'], pw['username'], pw['password'], '/home/jlmarks/if188start.csv', pw['apikey'])
a.prepareFile()
from robobrowser import RoboBrowser
a=RoboBrowser(history=True)
a.open('https://if188.infusionsoft.com')
lo=a.get_form()
lo.fields['username'].value=pw['username']
lo.fields['password'].value=pw['password']
a.submit_form(lo)
a.open('https://if188.infusionsoft.com/app/nav/link?navSystem=nav.admin&navModule=nav.admin.import')
a.response.content
lo=a.get_form()
lo
lo.fields
lo.fields.values
lo.fields.values()
lo.fields.values()[0]
lo.fields.values()[0].value
lo.fields['username'].value=pw['username']
lo.fields['password'].value=pw['password']
a.submit_form(lo)
a.response.content
print a.response.content
pw['username']
pw['password']
