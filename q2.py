import re
import sys


class NLUDefault:

    def __init__(self):
        self.oflavors = ["vegan", "hawaiian", "meat lovers", "4 cheese", "pepperoni", "veggie supreme"]
        self.osizes = ["small", "medium", "large"]
        self.ocrusts = ["thin", "regular", "gluten-free", "deep-dish"]
        self.Domain = "pizza"
        self.Intent = None
        self.Slots = {}
       
    def parse(self, inputStr):

    	#tokenized input string
    	tokenInput = inputStr.split()

        flavors = self.oflavors
        sizes = self.osizes
        crusts = self.ocrusts

        # Pizza info
        for flavor in flavors:
            if flavor in inputStr.lower():
                self.Intent = "INFORM"
                self.Slots["pizza_type"] = flavor
        for size in sizes:
            if size in inputStr.lower():
                self.Intent = "INFORM"
                self.Slots["pizza_size"] = size
        for crust in crusts:
            check_format = re.sub("-", "", crust)
            if crust in inputStr.lower() or check_format in inputStr.lower():
                self.Intent = "INFORM"
                self.Slots["pizza_crust"] = crust

        #NAMES
        if "it's" in inputStr:
        	


        #ADDRESSES

        #DELIVERY METHOD
        if "delivery" in inputStr.lower():
            self.Intent = "INFORM"
            self.Slots["order_delivery"] = "delivery"
        elif "pickup" in inputStr.lower() or "pick-up" in inputStr.lower():
            self.Intent = "INFORM"
            self.Slots["order_delivery"] = "pick-up"
        elif "takeout" in inputStr.lower() or "take-out" in inputStr.lower():
            self.Intent = "INFORM"
            self.Slots["order_delivery"] = "pick-up"

        #PHONE NUMBERS
     	if len(re.sub('[^0-9]','',inputStr)) == 10:
     		self.Intent = "INFORM"
            self.Slots["order_phone"] = re.sub('[^0-9]','',inputStr) 


        # Dialog flow control/User-initiative requests
        if "reorder" in inputStr.lower():
            self.Intent = "REORDER"
        elif "start-over" in inputStr.lower() or "startover" in inputStr.lower():
            self.Intent = "START-OVER"
        elif "cancel" in inputStr.lower():
            self.Intent = "CANCEL"
        elif "repeat" in inputStr.lower():
            self.Intent = "REPEAT"
        elif "check" in inputStr.lower():
            self.Intent = "CHECK_ORDER"

        # Confirm/deny
        if "yes" == inputStr or "Yes" == inputStr:
            self.Intent = "CONFIRM"
        elif "no" == inputStr or "No" == inputStr:
            self.Intent = "DENY"

    	return [self.Intent,self.annotatedStr]

in_string = input().lower()

