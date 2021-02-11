import re
import sys


class NLUDefault:

    def __init__(self):
        self.oflavors = ["vegan", "hawaiian", "meat lovers", "4 cheese", "pepperoni", "veggie supreme"]
        self.osizes = ["small", "medium", "large"]
        self.ocrusts = ["thin", "regular", "gluten-free", "deep-dish"]
        self.otoppings = ['onions','olives','swiss cheese','pineapple','provolone cheese','anchovies','extra cheese','peppers','pepporoni','sausage','ham','mushrooms']
        self.Domain = "pizza"
        self.Intent = None
        self.Slots = {}
       
    def parse(self, inputStr):

        #tokenized input string
    	tokenInput = inputStr.split()

    	#annotated string
    	annotatedStr = inputStr

        flavors = self.oflavors
        sizes = self.osizes
        crusts = self.ocrusts
        toppings = self.otoppings

        # Pizza info
        for flavor in flavors:
<<<<<<< HEAD
            inputStr, num_replace = re.sub(flavor, "<pizza_type>"+flavor+"</pizza_type>", inputStr)

            if num_replace > 0:
                self.Intent = "INFORM"

=======
            if inputStr.lower().find(flavor) != -1:
            	index_of_match = inputStr.lower().find(flavor)
            	end_of_match = inputStr.lower().find(flavor) + len(flavor)
                self.Intent = "INFORM"

                annotate_start = '<pizza_type>'
                annotate_end = '</pizza_type>'
                inputStr = inputStr[:index_of_match]  + annotate_start + inputStr[index_of_match:end_of_match] + annotate_end + inputStr[end_of_match:] 

                self.Slots["pizza_type"] = flavor
>>>>>>> 9589370a56063ecedd02638150655459a82e5f8d
        for size in sizes:
            inputStr, num_replace = re.sub(size, "<pizza_size>" + size + "</pizza_size>", inputStr)

            if num_replace > 0:
                self.Intent = "INFORM"

        size_regex = re.compile("[0-9]{2}.*(inch|in)")

        size = size_regex.search(inputStr).group(0)

        if size is not None:
            inputStr, num_replace = re.subn(size, "<pizza_size>" + size + "</pizza_size>", inputStr)
            self.Intent = "INFORM"

        for crust in crusts:
            inputStr, num_replace = re.sub(crust, "<pizza_crust>" + crust + "</pizza_crust>", inputStr)

            if num_replace > 0:
                self.Intent = "INFORM"

<<<<<<< HEAD
        for topping in toppings:
            inputStr, num_replace = re.sub(topping, "<pizza_topping>"+topping+"</pizza_topping>", inputStr)
=======
        #NAMES
        if "it's" in inputStr:


>>>>>>> 9589370a56063ecedd02638150655459a82e5f8d

            if num_replace > 0:
                self.Intent = "INFORM"

        #ADDRESSES
        address_regex = re.compile("[0-9]+ .* ([A|a]ve|[W|w]ay|[S|s]treet|[B|b]lvd)")

        address = address_regex.search(inputStr).group(0)

        inputStr, num_replace = re.subn(address, "<address>"+address+"</address>", inputStr)

        if num_replace > 0:
            self.Intent = "INFORM"


        #DELIVERY METHOD
        delivery_regex = re.compile("(delivery|delivered|deliver)")

        deliver = delivery_regex.search(inputStr).group(0)

        if deliver is not None:
            inputStr = re.sub(deliver, "<delivery_method>" + deliver + "</delivery_method>", inputStr)
            self.Intent = "INFORM"

        pickup_regex = re.compile("(pickup|pick-up|pick up|takeout|take-out|take out)")
        from_store_regex = re.compile("(?<=from your ).*(store|location)")

        pickup = pickup_regex.search(inputStr).group(0)

        if pickup is not None:
            inputStr = re.sub(pickup, "<delivery_method>" + pickup + "</delivery_method>", inputStr)
            self.Intent = "INFORM"

            from_store = pickup_regex.search(inputStr).group(0)

            if from_store is not None:
                inputStr = re.sub(from_store, "<pickup_location>" + from_store + "</pickup_location>", inputStr)
                self.Intent = "INFORM"


        #PHONE NUMBERS
        phone_number = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")

        number = phone_number.search(inputStr).group(0)

        if number is not None:
            inputStr, num_replace = re.subn(number, "<phone>"+number+"</phone>", inputStr)
            self.Intent = "INFORM"

        # NAMES
        if "it's" in inputStr:
            check = inputStr.split("it's ")
            if not check[1].startswith("<"):
                inputStr = re.sub(check[1], "<order_name>"+check[1]+"</order_name>", inputStr)
                self.Intent = "INFORM"
        if "this is" in inputStr:
            check = inputStr.split("this is ")
            tokenized_after = check[1].split()
            inputStr = re.sub(tokenized_after[0], "<order_name>"+tokenized_after[0]+"</order_name>", inputStr)
            self.Intent = "INFORM"

        # Dialog flow control/User-initiative requests
        reorder_check = re.compile("(reorder|usual|preferred)")
        if reorder_check.search(inputStr.lower()) is not None:
            self.Intent = "REORDER"

        startover_check = re.compile("(startover|start-over|start over)")
        cancel_check = re.compile("(cancel|stop|give up)")
        repeat_check = re.compile("(repeat|say that again|come again|what was that)")
        check_check = re.compile("(ready|when|where's the pizza i ordered)")




        if "start-over" in inputStr.lower() or "startover" in inputStr.lower():
            self.Intent = "START-OVER"
        elif "cancel" in inputStr.lower():
            self.Intent = "CANCEL"
        elif "repeat" in inputStr.lower():
            self.Intent = "REPEAT"
        elif "check" in inputStr.lower():
            self.Intent = "CHECK_ORDER"

        if self.Intent is None:
            hello_regex = re.compile("(hello|hey|how's it going|greetings|hi|yo)")

            hello = hello_regex.search(inputStr).group(0)

            if hello is not None:
                self.Intent = "HELLO"

        return self.Intent, inputStr


