#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-09-25 03:07:15
# @Last Modified 2015-09-28
# @Last Modified time: 2015-09-28 01:05:15

# This is the main script for  Project Treadstone.

import os                                   # Since I am working in the file system so much, it is
                                            # super easy and helpful to be able to access the operating
                                            # system directly.
import csv                                  # because we're using csvs, ya know?
import xmlrpclib                            # This is needed to interact with the API
import uuid                                 # This is so that we can generate UUIDs
from datetime import datetime               # So that we can work with dates in one nice way.

from bs4 import BeautifulSoup               # This is the HTML parser I use
from robobrowser import RoboBrowser         # This is the "browser" that I use
from local import settings                  # This is where I am storing variables for dev purposes

import dropdownmatching

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#############################################
## So, it is quickly going to be obvious that I don't know
## UX/UI stuff.  This is my meager attempt toward that.
import Tkinter as tk
import tkFileDialog
tk.Tk().withdraw()


def getFilePath():
    return tkFileDialog.askopenfilename()


#############################################
## These are the options that are available
## when importing the file through the front
## end.
#############################################

subsImportAvailCols={}
subsImportAvailCols["Do NOT import this field"] = {"required": False, "helpText": "If you want to not import this column"}
subsImportAvailCols["Your System's Subscription Id"] = {"required": False, "helpText": "Generally avoid this. If you jack up an import, you will have to remove it anyway."}
subsImportAvailCols["Infusionsoft's Contact Id"] = {"required": True, "helpText": "If you have a subscription, someone has to pay for it.  This is that someone."}
subsImportAvailCols["Subscription Plan Id"] = {"required": True, "helpText": "This is the Id of the actual subscription plan that you are using. It is the \"Every 3 weeks for 1 week\" part of the product."}
subsImportAvailCols["Product Id"] = {"required": True, "helpText": "Yeah, yeah, the subscription plan id is unique and can only be tied to one product. Why do we need the product id?  That is a great question. You can await my reply if you like. "}
subsImportAvailCols["Program Id"] = {"required": False, "helpText": "Pretty sure that this is required.  It is the Id from the CProgram table"}
subsImportAvailCols["Infusionsoft's Lead Affiliate Id"] = {"required": False, "helpText": "You know the drill"}
subsImportAvailCols["Infusionsoft's Sale Affiliate Id"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Credit Card Id"] = {"required": False, "helpText": "While it is not required, I think that it is required that the card be owned by the contact"}
subsImportAvailCols["Payment Gateway Id"] = {"required": False, "helpText": "This needs to be the merchatn account id"}
subsImportAvailCols["Frequency"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Cycle"] = {"required": True, "helpText": "Must be one of the following numbers: 6 (Daily) - 2 (Month) - 3 (Weekly) - 1 (Year)"}
subsImportAvailCols["Price"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Promo Code"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Order Type"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Status"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Start Date"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["End Date"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Reason Stopped"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Paid Thru Date"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Auto Charge"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Max Charge Attempts"] = {"required": False, "helpText": "SomeStringHere"}
subsImportAvailCols["Num Days Between Retry"] = {"required": False, "helpText": "SomeStringHere"}



###########################################################
## This next section is poorly documented, however I think
## that it is clear what it does and how it works.
## If you disagree, please let me know!
##
## ISServer is the main tool that I use to interact with the
## Infusionsoft API.
##
## "tables" is a data structure that uses table names as keys
## to an array of column names as its value.
###########################################################


class ISServer:
    def __init__(self, appname, apikey):
        global settings
        self.pw = settings
        self.startingpath = os.path.abspath(os.curdir)
        self.infusionsoftapp=appname
        self.baseurl = 'https://' + self.infusionsoftapp + '.infusionsoft.com/'
        self.infusionsoftAPIKey=apikey
        self.appurl = "https://" + self.infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"
        self.connection = xmlrpclib.ServerProxy(self.appurl)
        self.browser = RoboBrowser(history=True)

    def getappname(self):
        return raw_input("Please enter appname:").strip('\n \t')
    def getapikey(self):
        global pw
        username = self.pw['username']
        password = self.pw['password']
        #Basically:
        #    #Add username and password to your global variables.
        self.browser.open(self.baseurl)
        logform = self.browser.get_form()
        logform.fields['username'].value = username
        logform.fields['password'].value = password
        self.browser.submit_form(logform)
        self.browser.follow_link(self.browser.get_links()[1])
        self.browser.open(self.baseurl + 'app/miscSetting/itemWrapper?systemId=nav.admin&settingModuleName=Application&settingTabName=Application')
        pageSoup = BeautifulSoup(self.browser.response.content, 'html.parser')
        return pageSoup.findAll(id='Application_Encrypted_Key:_data')[0].text
    ########################################################
    ## Methods to get records from various tables
    ##
    ##
    def getMatchingRecords(self, tableName, criteria, desiredFields=None, orderedBy=None):
        """Search at table by criteria
        """
        return self.getAllRecords(tableName, searchCriteria=criteria, interestingData=desiredFields, orderedBy=orderedBy)
    def getTagCats(self):
        return self.getAllRecords("ContactGroupCategory")
    def getAllTags(self):
        return self.getAllRecords("ContactGroup")
    def getAllProductCats(self):
        return self.getAllRecords("ProductCategory")
    def getAllProducts(self):
        return self.getAllRecords("Product")
    def getAllRecords(self, tableName, interestingData=None, searchCriteria=None, orderedBy=None):
        if interestingData is None:
            interestingData = tables[tableName]
        if searchCriteria is None:
            searchCriteria={}
        if orderedBy is None:
            orderedBy = interestingData[0]
        records = []
        p=0
        while True:
            listOfDicts = self.connection.DataService.query(self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
            for each in listOfDicts:
                thisRecord={}
                for eachbit in interestingData:   # this should be records.append(zip(interestingData, each)) perhaps
                    if not each.has_key(eachbit):   # TODO: research THIS
                        each[eachbit]=None
                    thisRecord[eachbit] = each[eachbit]
                records.append(thisRecord)
            if not(len(listOfDicts)==1000):
                break
            p+=1
        return records
    def incrementlyGetRecords(self, tableName, interestingData=None, searchCriteria=None, orderedBy=None):
        if interestingData is None:
            interestingData = tables[tableName]
        if searchCriteria is None:
            searchCriteria={}
        if orderedBy is None:
            orderedBy = interestingData[0]
        records = []
        p=0
        while True:
            print tableName, p
            print "trying!"
            try:
                listOfDicts = self.connection.DataService.query(self.infusionsoftAPIKey, tableName, 1000, p, searchCriteria, interestingData, orderedBy, True)
            except Exception, e:
                print e ,p
            for each in listOfDicts:
                thisRecord={}
                for eachbit in interestingData:   # this should be records.append(zip(interestingData, each)) perhaps
                    if not each.has_key(eachbit):   # TODO: research THIS
                        each[eachbit]=None
                    thisRecord[eachbit] = each[eachbit]
                records.append(thisRecord)
            if not(len(listOfDicts)==1000):
                break
            p+=1
            if p%10==0:
                fname = tableName + "%010d" %(p) + ".csv"
                print 'writing', p, fname
                with open(fname, 'wb') as outfile:
                    thisWriter = csv.DictWriter(outfile, records[0])
                    thisWriter.writeheader()
                    thisWriter.writerows(records)
                records=[]
        fname = tableName + "%010d" %(p) + ".csv"
        print 'writing', p, fname
        with open(fname, 'wb') as outfile:
            thisWriter = csv.DictWriter(outfile, records[0])
            thisWriter.writeheader()
            thisWriter.writerows(records)
    def log(self, text):
        with open('issvr.log', 'a') as logfile:
            logfile.write(text + "\n")

    def incgetfiles(self):
        browser = self.browser
        self.curdir = os.path.abspath(os.path.curdir)
        p=0
        while True:
            print "Doing page " + str(p)
            try:
                listofdicts =  self.connection.DataService.query(self.infusionsoftAPIKey, 'FileBox', 1000, p, {}, tables["FileBox"], 'Id', False)
                for eachfile in listofdicts:
                    try:
                        downloadurl = self.baseurl + "/Download?Id=" + str(eachfile['Id'])
                        browser.open(downloadurl)
                        # folderpath = os.path.abspath(os.path.join(self.curdir, 'files', str(eachfile['ContactId']) ))
                        fileoutpath = os.path.abspath(os.path.join(self.curdir, 'files', str(eachfile['ContactId'])))
                        if not os.path.exists(fileoutpath):
                            os.makedirs(fileoutpath)
                        fileoutpath = os.path.abspath(os.path.join(fileoutpath, '%09d' %(int(eachfile['Id'])) + eachfile['FileName']))
                        fout = open(fileoutpath, 'wb')
                        fout.write(browser.response.content)
                        fout.close()
                    except Exception, e:
                        self.log(str(e))
                        self.log(str(eachfile))
                        print eachfile,'\n', e
            except Exception, e:
                print p, e
            finally:
                if not (len(listofdicts)==1000):
                    break
                else:
                    p+=1
    def cnp(self, productValues):
        return self.createNewRecord('Product', productValues)
    def createNewRecord(self, table, recordvalues):
        return self.connection.DataService.add(self.infusionsoftAPIKey, table, recordvalues)
    ########################################################
    ## Methods to updating existing records
    ##
    def updateRecord(self, tableName, recordId, updateValues):
        return self.connection.DataService.update(self.infusionsoftAPIKey, tableName, recordId, updateValues)
    def deleteRecordsOnTable(self, tableName):
        allTableIds=self.getAllRecords(tableName, ["Id"])
        for eachid in allTableIds:
            try:
                self.connection.DataService.delete(tablename, eachid)
            except:
                print "Cannot Delete " + str(eachid)

    ########################################################
    ## Method to create a new contact record, or updates an existing
    ## potential values for checktype are
    ## ['Email', 'EmailAndName', 'EmailAndNameAndCompany']
    def dupeCreate(self, contactData={}, checktype='Email'):
        return self.connection.ContactService.addWithDupCheck(self.infusionsoftAPIKey, contactData, checktype)

    ########################################################
    ## Methods to get meta-data about records
    def getCount(self, tableName, query):
        return self.connection.DataService.count(self.infusionsoftAPIKey, tableName, query)
    def verifyConnection(self):
        try:
            listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, "User", 1000, 0,{},["Email"],"Email",True)
            return True
        except:
            return False



tables={}
# This is a dictionary of the tables accessiable through the API
# It has not been fully sanitized with regards to permissions, so you
# Will likely run into issues where you cannot read something
# but you may be able to write to it, or visa-versa.  Basically,
# until you have worked with a specific table a couple of times,
# expect to run into errors.
tables["ActionSequence"] = ["Id", "TemplateName", "VisibleToTheseUsers"]
tables["AffResource"] = ["Id", "Notes", "ProgramIds", "ResourceHREF", "ResourceHTML", "ResourceOrder", "ResourceType", "Title"]
tables["Affiliate"] = ["AffCode", "AffName", "ContactId", "DefCommissionType", "Id", "LeadAmt", "LeadCookieFor", "LeadPercent", "NotifyLead", "NotifySale", "ParentId", "Password", "PayoutType", "SaleAmt", "SalePercent", "Status"]
tables["CCharge"] = ["Amt", "ApprCode", "CCId", "Id", "MerchantId", "OrderNum", "PaymentId", "RefNum"]
tables["CProgram"] = ["Active", "BillingType", "DefaultCycle", "DefaultFrequency", "DefaultPrice", "Description", "Family", "HideInStore", "Id", "LargeImage", "ProductId", "ProgramName", "ShortDescription", "Sku", "Status", "Taxable"]
tables["Campaign"] = ["Id", "Name", "Status"]
tables["CampaignStep"] = ["CampaignId", "Id", "StepStatus", "StepTitle", "TemplateId"]
tables["Campaignee"] = ["Campaign", "CampaignId", "ContactId", "Status"]
tables["Company"] = ["AccountId", "Address1Type", "Address2Street1", "Address2Street2", "Address2Type", "Address3Street1", "Address3Street2", "Address3Type", "Anniversary", "AssistantName", "AssistantPhone", "BillingInformation", "Birthday", "City", "City2", "City3", "Company", "CompanyID", "ContactNotes", "ContactType", "Country", "Country2", "Country3", "CreatedBy", "DateCreated", "Email", "EmailAddress2", "EmailAddress3", "Fax1", "Fax1Type", "Fax2", "Fax2Type", "FirstName", "Groups", "Id", "JobTitle", "LastName", "LastUpdated", "LastUpdatedBy", "MiddleName", "Nickname", "OwnerID", "Password", "Phone1", "Phone1Ext", "Phone1Type", "Phone2", "Phone2Ext", "Phone2Type", "Phone3", "Phone3Ext", "Phone3Type", "Phone4", "Phone4Ext", "Phone4Type", "Phone5", "Phone5Ext", "Phone5Type", "PostalCode", "PostalCode2", "PostalCode3", "ReferralCode", "SpouseName", "State", "State2", "State3", "StreetAddress1", "StreetAddress2", "Suffix", "Title", "Username", "Validated", "Website", "ZipFour1", "ZipFour2", "ZipFour3"]
tables["Contact"] = ["AccountId", "Address1Type", "Address2Street1", "Address2Street2", "Address2Type", "Address3Street1", "Address3Street2", "Address3Type", "Anniversary", "AssistantName", "AssistantPhone", "BillingInformation", "Birthday", "City", "City2", "City3", "Company", "CompanyID", "ContactNotes", "ContactType", "Country", "Country2", "Country3", "CreatedBy", "DateCreated", "Email", "EmailAddress2", "EmailAddress3", "Fax1", "Fax1Type", "Fax2", "Fax2Type", "FirstName", "Groups", "Id", "JobTitle", "LastName", "LastUpdated", "LastUpdatedBy", "LeadSourceId", "Leadsource", "MiddleName", "Nickname", "OwnerID", "Password", "Phone1", "Phone1Ext", "Phone1Type", "Phone2", "Phone2Ext", "Phone2Type", "Phone3", "Phone3Ext", "Phone3Type", "Phone4", "Phone4Ext", "Phone4Type", "Phone5", "Phone5Ext", "Phone5Type", "PostalCode", "PostalCode2", "PostalCode3", "ReferralCode", "SpouseName", "State", "State2", "State3", "StreetAddress1", "StreetAddress2", "Suffix", "Title", "Username", "Validated", "Website", "ZipFour1", "ZipFour2", "ZipFour3"]
tables["ContactAction"] = ["Accepted", "ActionDate", "ActionDescription", "ActionType", "CompletionDate", "ContactId", "CreatedBy", "CreationDate", "CreationNotes", "EndDate", "Id", "IsAppointment", "LastUpdated", "LastUpdatedBy", "ObjectType", "OpportunityId", "PopupDate", "Priority", "UserID"]
tables["ContactGroup"] = ["GroupCategoryId", "GroupDescription", "GroupName", "Id"]
tables["ContactGroupAssign"] = ["Contact.Address1Type", "Contact.Address2Street1", "Contact.Address2Street2", "Contact.Address2Type", "Contact.Address3Street1", "Contact.Address3Street2", "Contact.Address3Type", "Contact.Anniversary", "Contact.AssistantName", "Contact.AssistantPhone", "Contact.BillingInformation", "Contact.Birthday", "Contact.City", "Contact.City2", "Contact.City3", "Contact.Company", "Contact.CompanyID", "Contact.ContactNotes", "Contact.ContactType", "Contact.Country", "Contact.Country2", "Contact.Country3", "Contact.CreatedBy", "Contact.DateCreated", "Contact.Email", "Contact.EmailAddress2", "Contact.EmailAddress3", "Contact.Fax1", "Contact.Fax1Type", "Contact.Fax2", "Contact.Fax2Type", "Contact.FirstName", "Contact.Groups", "Contact.Id", "Contact.JobTitle", "Contact.LastName", "Contact.LastUpdated", "Contact.LastUpdatedBy", "Contact.Leadsource", "Contact.MiddleName", "Contact.Nickname", "Contact.OwnerID", "Contact.Phone1", "Contact.Phone1Ext", "Contact.Phone1Type", "Contact.Phone2", "Contact.Phone2Ext", "Contact.Phone2Type", "Contact.Phone3", "Contact.Phone3Ext", "Contact.Phone3Type", "Contact.Phone4", "Contact.Phone4Ext", "Contact.Phone4Type", "Contact.Phone5", "Contact.Phone5Ext", "Contact.Phone5Type", "Contact.PostalCode", "Contact.PostalCode2", "Contact.PostalCode3", "Contact.ReferralCode", "Contact.SpouseName", "Contact.State", "Contact.State2", "Contact.State3", "Contact.StreetAddress1", "Contact.StreetAddress2", "Contact.Suffix", "Contact.Title", "Contact.Website", "Contact.ZipFour1", "Contact.ZipFour2", "Contact.ZipFour3", "ContactGroup", "ContactId", "DateCreated", "GroupId"]
tables["ContactGroupCategory"] = ["CategoryDescription", "CategoryName", "Id"]
tables["CreditCard"] = ["BillAddress1", "BillAddress2", "BillCity", "BillCountry", "BillName", "BillState", "BillZip", "CardType", "ContactId", "Email", "ExpirationMonth", "ExpirationYear", "FirstName", "Id", "Last4", "LastName", "MaestroIssueNumber", "NameOnCard", "PhoneNumber", "ShipAddress1", "ShipAddress2", "ShipCity", "ShipCompanyName", "ShipCountry", "ShipFirstName", "ShipLastName", "ShipMiddleName", "ShipName", "ShipPhoneNumber", "ShipState", "ShipZip", "StartDateMonth", "StartDateYear", "Status"]
tables["DataFormField"] = ["DataType", "DefaultValue", "FormId", "GroupId", "Id", "Label", "ListRows", "Name", "Values"]
tables["DataFormGroup"] = ["Id", "Name", "TabId"]
tables["DataFormTab"] = ["FormId", "Id", "TabName"]
tables["Expense"] = ["ContactId", "DateIncurred", "ExpenseAmt", "ExpenseType", "Id", "TypeId"]
tables["FileBox"] = ["ContactId", "Extension", "FileName", "FileSize", "Id", "Public"]
tables["GroupAssign"] = ["Admin", "GroupId", "Id", "UserId"]
tables["Invoice"] = ["AffiliateId", "ContactId", "CreditStatus", "DateCreated", "Description", "Id", "InvoiceTotal", "InvoiceType", "JobId", "LeadAffiliateId", "PayPlanStatus", "PayStatus", "ProductSold", "PromoCode", "RefundStatus", "Synced", "TotalDue", "TotalPaid"]
tables["InvoiceItem"] = ["CommissionStatus", "DateCreated", "Description", "Discount", "Id", "InvoiceAmt", "InvoiceId", "OrderItemId"]
tables["InvoicePayment"] = ["Amt", "Id", "InvoiceId", "PayDate", "PayStatus", "PaymentId", "SkipCommission"]
tables["Job"] = ["ContactId", "DateCreated", "DueDate", "Id", "JobNotes", "JobRecurringId", "JobStatus", "JobTitle", "OrderStatus", "OrderType", "ProductId", "StartDate"]
tables["JobRecurringInstance"] = ["AutoCharge", "DateCreated", "Description", "EndDate", "Id", "InvoiceItemId", "RecurringId", "StartDate", "Status"]
tables["Lead"] = ["AffiliateId", "ContactID", "CreatedBy", "DateCreated", "EstimatedCloseDate", "Id", "LastUpdated", "LastUpdatedBy", "Leadsource", "NextActionDate", "NextActionNotes", "Objection", "OpportunityNotes", "OpportunityTitle", "ProjectedRevenueHigh", "ProjectedRevenueLow", "StageID", "StatusID", "UserID"]
tables["LeadSource"] = ["CostPerLead", "Description", "EndDate", "Id", "LeadSourceCategoryId", "Medium", "Message", "Name", "StartDate", "Status", "Vendor"]
tables["LeadSourceCategory"] = ["Description", "Id", "Name"]
tables["LeadSourceExpense"] = ["Amount", "DateIncurred", "Id", "LeadSourceId", "LeadSourceRecurringExpenseId", "Notes", "Title"]
tables["LeadSourceRecurringExpense"] = ["Amount", "EndDate", "Id", "LeadSourceId", "NextExpenseDate", "Notes", "StartDate", "Title"]
tables["MtgLead"] = ["ActualCloseDate", "ApplicationDate", "CreditReportDate", "DateAppraisalDone", "DateAppraisalOrdered", "DateAppraisalReceived", "DateRateLockExpires", "DateRateLocked", "DateTitleOrdered", "DateTitleReceived", "FundingDate", "Id"]
tables["OrderItem"] = ["CPU", "Id", "ItemDescription", "ItemName", "ItemType", "Notes", "OrderId", "PPU", "ProductId", "Qty", "SubscriptionPlanId"]
tables["PayPlan"] = ["AmtDue", "DateDue", "FirstPayAmt", "Id", "InitDate", "InvoiceId", "StartDate", "Type"]
tables["PayPlanItem"] = ["AmtDue", "AmtPaid", "DateDue", "Id", "PayPlanId", "Status"]
tables["Payment"] = ["ChargeId", "Commission", "ContactId", "Id", "InvoiceId", "PayAmt", "PayDate", "PayNote", "PayType", "RefundId", "Synced", "UserId"]
tables["Product"] = ["BottomHTML", "CityTaxable", "CountryTaxable", "Description", "HideInStore", "Id", "InventoryLimit", "InventoryNotifiee", "IsPackage", "LargeImage", "NeedsDigitalDelivery", "ProductName", "ProductPrice", "Shippable", "ShippingTime", "ShortDescription", "Sku", "StateTaxable", "Status", "Taxable", "TopHTML", "Weight"]
tables["ProductCategory"] = ["CategoryDisplayName", "CategoryImage", "CategoryOrder", "Id", "ParentId"]
tables["ProductCategoryAssign"] = ["Id", "ProductCategoryId", "ProductId"]
tables["ProductInterest"] = ["DiscountPercent", "Id", "ObjType", "ObjectId", "ProductId", "ProductType", "Qty"]
tables["ProductInterestBundle"] = ["BundleName", "Description", "Id"]
tables["ProductOptValue"] = ["Id", "IsDefault", "Label", "Name", "OptionIndex", "PriceAdjustment", "ProductOptionId", "Sku"]
tables["ProductOption"] = ["AllowSpaces", "CanContain", "CanEndWith", "CanStartWith", "Id", "IsRequired", "Label", "MaxChars", "MinChars", "Name", "OptionType", "Order", "ProductId", "TextMessage"]
tables["RecurringOrder"] = ["AffiliateId", "AutoCharge", "BillingAmt", "BillingCycle", "CC1", "CC2", "ContactId", "EndDate", "Frequency", "Id", "LastBillDate", "LeadAffiliateId", "MaxRetry", "MerchantAccountId", "NextBillDate", "NumDaysBetweenRetry", "OriginatingOrderId", "PaidThruDate", "ProductId", "ProgramId", "PromoCode", "Qty", "ReasonStopped", "ShippingOptionId", "StartDate", "Status", "SubscriptionPlanId"]
tables["RecurringOrderWithContact"] = ["AffiliateId", "AutoCharge", "BillingAmt", "BillingCycle", "CC1", "CC2", "City", "ContactId", "ContactId", "Country", "Email", "EmailAddress2", "EmailAddress3", "EndDate", "FirstName", "Frequency", "LastBillDate", "LastName", "LeadAffiliateId", "MaxRetry", "MerchantAccountId", "MiddleName", "NextBillDate", "Nickname", "NumDaysBetweenRetry", "PaidThruDate", "Phone1", "Phone1Ext", "Phone1Type", "Phone2", "Phone2Ext", "Phone2Type", "PostalCode", "ProductId", "ProgramId", "PromoCode", "Qty", "ReasonStopped", "RecurringOrderId", "ShippingOptionId", "SpouseName", "StartDate", "State", "Status", "StreetAddress1", "StreetAddress2", "SubscriptionPlanId", "Suffix", "Title", "ZipFour1"]
tables["Referral"] = ["AffiliateId", "ContactId", "DateExpires", "DateSet", "IPAddress", "Id", "Info", "Source", "Type"]
tables["SavedFilter"] = ["FilterName", "Id", "ReportStoredName", "UserId"]
tables["Stage"] = ["Id", "StageName", "StageOrder", "TargetNumDays"]
tables["StageMove"] = ["CreatedBy", "DateCreated", "Id", "MoveDate", "MoveFromStage", "MoveToStage", "OpportunityId", "PrevStageMoveDate", "UserId"]
tables["Status"] = ["Id", "StatusName", "StatusOrder", "TargetNumDays"]
tables["SubscriptionPlan"] = ["Active", "Cycle", "Frequency", "Id", "PlanPrice", "PreAuthorizeAmount", "ProductId", "Prorate"]
tables["Template"] = ["Categories", "Id", "PieceTitle", "PieceType"]
tables["TicketStage"] = ["Id", "StageName"]
tables["TicketType"] = ["CategoryId", "Id", "Label"]
tables["User"] = ["City", "Email", "EmailAddress2", "EmailAddress3", "FirstName", "HTMLSignature", "Id", "LastName", "MiddleName", "Nickname", "Phone1", "Phone1Ext", "Phone1Type", "Phone2", "Phone2Ext", "Phone2Type", "PostalCode", "Signature", "SpouseName", "State", "StreetAddress1", "StreetAddress2", "Suffix", "Title", "ZipFour1"]
tables["UserGroup"] = ["Id", "Name", "OwnerId"]

###########################################################
###########################################################
###########################################################
#   This is where various methods will reside specific to
#   this project.  They may get added to other projects,
#   But this is where they live for now.
###########################################################
###########################################################
###########################################################
def findSubByUUIDInReasonStopped(apiConnection, uuid):
    """This method is useful if you have stashed a uuid
    in the ReasonStopped field.
    """
    return apiConnection.getAllRecords('RecurringOrder', searchCriteria={'ReasonStopped': '%'+uuid+'%'})
def prepareForInvoices(apiConnection, subscriptionId):
    """This method will serve to remove the end date from a
    subscription. If there is no existing end date, it will
    return None.

    It was going to return the original end date, however I
    would rather save the API calls and assume that you
    were able to get that at the same time you found the
    subscriptionId
    """
    return apiConnection.updateRecord('RecurringOrder', subscriptionId, {"AutoCharge": 1, 'EndDate': ''})

####
#  recurringOrder=tcon.getAllRecords('RecurringOrder', searchCriteria={'Id': 131})



def deleteInvoicesForSubscriptions(apiConnection, subscriptionId, deleteAfter=None):
    jobsData = apiConnection.getAllRecords('Job', searchCriteria={'JobRecurringId': subscriptionId})
    for eachJob in jobsData:
        duedate = datetime.strptime(eachJob['DueDate'].value, '%Y%m%dT%H:%M:%S')
        if deleteAfter is None or duedate>deleteAfter:
            invoiceData = apiConnection.getAllRecords('Invoice', searchCriteria={'JobId': eachJob['Id']})
            if len(invoiceData) > 0:
                for eachInvoice in invoiceData:
                    apiConnection.connection.InvoiceService.deleteInvoice(settings['apikey'], eachInvoice['Id'])

class importError(object):
    def __init__(self, message, context=None):
        self.timestamp = datetime.now().strftime("%Y%b%d %H:%M:%S").replace(' ', '').replace(':', '')
        self.message = message
        if context is None:
            self.context = "Whelp, you're a dumbass."
        else:
            self.context = str(context)



class HisSubImp(object):
    """This is the historic Import tool.  Yay!
    It will be started by passing it the name of an application.
    If you are on the IS network and have your credentials set
    up properly, that is all that you will need to pass it.
    If not, you will need to pass it the username and password
    for the application.
    """
    def __init__(self, appname, username, password, pathtocsv, apikey):
        self.appname = appname
        self.username = username
        self.password = password
        self.apikey = apikey
        self.pathtocsv = pathtocsv
        self.api=ISServer(appname, apikey)
        self.starttime = self.gettimestamp()
        self.log=[]
        self.startfolder = os.path.abspath(os.path.curdir)
        self.applicationfolder = os.path.abspath(os.path.join(os.path.abspath(os.path.curdir), appname))
        if not os.path.exists(self.applicationfolder):
            os.makedirs(self.applicationfolder)
        elif os.path.isfile(self.applicationfolder):
            newpath = os.path.abspath(os.path.join(os.path.abspath(os.path.curdir), appname + "FOLDER"))
            log.append(importError("Path" + str(self.applicationfolder) + " exists as a file. Using " + str(newpath) + " instead."))
            self.applicationfolder = newpath
            if not os.path.exists(self.applicationfolder):
                os.makedirs(self.applicationfolder)
        os.chdir(self.applicationfolder)
        self.idlog = os.path.abspath(os.path.join(os.path.abspath(self.applicationfolder), 'largestids.csv'))
        self.instancefolder = os.path.abspath(os.path.join(os.path.abspath(os.path.curdir), self.starttime))
        os.makedirs(self.instancefolder)
        os.chdir(self.instancefolder)
        self.startvals = self.tableSnapshot()

    def gettimestamp(self):
        return datetime.now().strftime("%Y%b%d %H:%M:%S").replace(' ', '').replace(':', '')

    def getmaxid(self, table):
        # basically:
        numberofrecords = 1
        pagetogetrecordfrom = 0
        searchCriteria = {}
        interestingData = ['Id']
        sortby = interestingData
        lowestfirst=False
        largestrecord = self.api.connection.DataService.query(self.apikey,
                                                     table, numberofrecords,
                                                     pagetogetrecordfrom,
                                                     searchCriteria, interestingData,
                                                     sortby, lowestfirst)[0]['Id']
        self.updatemaxrecordfile(table, largestrecord)
        return largestrecord

    def updatemaxrecordfile(self, tablename, maxid):
        record={}
        record['currenttime'] = self.gettimestamp()
        record['tablename'] = tablename
        record['maxid'] = maxid
        if not os.path.exists(self.idlog):
            with open(self.idlog, 'wb') as outfile:
                thiswriter = csv.DictWriter(outfile, record.keys())
                thiswriter.writeheader()
        with open(self.idlog, 'a+') as loggedfile:
            thiswriter=csv.DictWriter(loggedfile, record.keys())
            thiswriter.writerow(record)

    def tableSnapshot(self):
        snapshot={}
        snapshot['timestamp'] = self.gettimestamp()
        for eachtable in ["CCharge", "CProgram", "Contact", "CreditCard", "Invoice", "InvoiceItem", "InvoicePayment", "Job", "JobRecurringInstance", "PayPlan", "PayPlanItem", "Payment", "RecurringOrder", "SubscriptionPlan"]:
            snapshot[eachtable] = self.getmaxid(eachtable)
        return snapshot


    def prepareFile(self):
        self.importfile = os.path.join(os.path.abspath(self.instancefolder), self.gettimestamp() + ".csv")
        with open(self.pathtocsv, 'rb') as infile:
            mainreader = csv.DictReader(infile)
            infields = list(mainreader.fieldnames)
            if 'PromoCode' not in infields:
                outfields = infields + ['PromoCode', ]
            else:
                outfields = infields[:]
            with open(self.importfile, 'wb') as outfile:
                thiswriter = csv.DictWriter(outfile, outfields)
                thiswriter.writeheader()
                for eachrow in mainreader:
                    newrow = dict(eachrow)
                    newrow["PromoCode"] = str(uuid.uuid4())
                    #############
                    ## I figure I can add it back through the API later, since I have the original file.
                    #############
                    # if "PromoCode" in newrow.keys():
                    #     newrow["PromoCode"] = str(uuid.uuid4()) + newrow["PromoCode"]
                    # else:
                    #     newrow["PromoCode"] = str(uuid.uuid4())
                    thiswriter.writerow(newrow)

    def olduploadfile(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get("https://" + self.appname + ".infusionsoft.com/")
        elem = self.driver.find_element_by_id('username')
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id('password')
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        self.driver.get("https://" + self.appname + ".infusionsoft.com/Import/jumpToWizard.jsp?update=false&profileClass=com.infusion.crm.db.importer.profiles.ROrderProfile")
        self.driver.find_element_by_id("importFile").send_keys(self.importfile)
        self.driver.find_element_by_id("Submit").click()
        self.driver.find_element_by_id("Submit").click()
        self.driver.find_element_by_id("Submit").click()
        self.driver.find_element_by_id("Submit").click()

    def uploadfile(self, newfile=False):
        # This is going to assume that column matching will just happen
        if newfile:
            filetoupload = getFilePath()
        else:
            filetoupload = self.importfile
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get("https://" + self.appname + ".infusionsoft.com/")
        elem = self.driver.find_element_by_id('username')
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id('password')
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        self.driver.get("https://" + self.appname + ".infusionsoft.com/Import/jumpToWizard.jsp?update=false&profileClass=com.infusion.crm.db.importer.profiles.ROrderProfile")
        driver.find_element_by_id("importFile").send_keys(filetoupload)
        driver.find_element_by_id("Submit").click()
        ##################################################################
        ##
        ##
        ##  Matching columns still needs to happen here.
        ##
        ##
        ####################################################################


# I have no clue what this will do....

###########################################################
###########################################################
###########################################################
#
#   Below here are only methods that I use to test
#   individual parts of the script as I am building it
#   If I am good about it, they should be name sequentially
#   And that is all that should exist below this line.
###########################################################
###########################################################
###########################################################




def v1():
    modifiedData=[] # This is to store the csv data after it has been modified
    with open(settings['inputcsv'], 'rb') as infile:
        thisreader = csv.DictReader(infile)
        for eachline in thisreader:
            thisrow = dict(eachline)
            if 'PromoCode' not in thisrow.keys():
                thisrow['PromoCode']=""
            thisrow['PromoCode']+=str(uuid.uuid4())
            # Lets take this(Promocode) out at first, and then put it back later
            modifiedData.append(thisrow)
    with open(settings['outputcsv'], 'wb') as outfile:
        thiswriter = csv.DictWriter(outfile, modifiedData[0].keys())
        thiswriter.writeheader()
        thiswriter.writerows(modifiedData)
    raw_input("Please import the file and press enter after it has completed processing!")

def v2():
    apiConnection = ISServer(settings['appname'], settings['apikey'])
    thissub = findSubByUUIDInReasonStopped(apiConnection, "37ab5c71-0bdf-43d1-9bde-26054d705213")
    if len(thissub) >1:
        print "Many found for, using first."
    prepareForInvoices(apiConnection, thissub[0]['Id'])
    apiConnection.connection.InvoiceService.createInvoiceForRecurring(settings['apikey'], thissub[0]['Id'])




