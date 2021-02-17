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

			inputStr, num_replace = re.subn(flavor, "<pizza_type>"+flavor+"</pizza_type>", inputStr)

			if num_replace > 0:
				self.Intent = "INFORM"

		for size in sizes:
			inputStr, num_replace = re.subn(size, "<pizza_size>" + size + "</pizza_size>", inputStr)

			if num_replace > 0:
				self.Intent = "INFORM"

		size_regex = re.compile("[0-9]{2}.*(inch|in)")

		size = size_regex.search(inputStr)

		if size is not None:
			size = size.group(0)
			inputStr, num_replace = re.subn(size, "<pizza_size>" + size + "</pizza_size>", inputStr)
			self.Intent = "INFORM"

		for crust in crusts:
			inputStr, num_replace = re.subn(crust, "<pizza_crust>" + crust + "</pizza_crust>", inputStr)

			if num_replace > 0:
				self.Intent = "INFORM"

		for topping in toppings:
			inputStr, num_replace = re.subn(topping, "<pizza_topping>"+topping+"</pizza_topping>", inputStr)


			if num_replace > 0:
				self.Intent = "INFORM"

		#ADDRESSES
		address_regex = re.compile("[0-9]+ .* ([A|a]ve|[W|w]ay|[S|s]treet|[B|b]lvd)")

		address = address_regex.search(inputStr)

		if address is not None:
			address = address.group(0)
			inputStr, num_replace = re.subn(address, "<address>"+address+"</address>", inputStr)

			if num_replace > 0:
				self.Intent = "INFORM"


		#DELIVERY METHOD
		delivery_regex = re.compile("(delivery|delivered|deliver)")

		deliver = delivery_regex.search(inputStr)

		if deliver is not None:
			deliver = deliver.group(0)
			inputStr = re.sub(deliver, "<delivery_method>" + deliver + "</delivery_method>", inputStr)
			self.Intent = "INFORM"

		pickup_regex = re.compile("(pickup|pick-up|pick up|takeout|take-out|take out)")
		from_store_regex = re.compile("(?<=from your ).*(store|location)")

		pickup = pickup_regex.search(inputStr)

		if pickup is not None:
			pickup = pickup.group(0)
			inputStr = re.sub(pickup, "<delivery_method>" + pickup + "</delivery_method>", inputStr)
			self.Intent = "INFORM"

			from_store = pickup_regex.search(inputStr)

			if from_store is not None:
				from_store = from_store.group(0)
				inputStr = re.sub(from_store, "<pickup_location>" + from_store + "</pickup_location>", inputStr)
				self.Intent = "INFORM"


		#PHONE NUMBERS
		phone_number = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")

		number = phone_number.search(inputStr)

		if number is not None:
			number = number.group(0)
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

		if startover_check.search(inputStr) != None:
			self.Intent = "START-OVER"
		elif cancel_check.search(inputStr) != None:
			self.Intent = "CANCEL"
		elif repeat_check.search(inputStr) != None:
			self.Intent = "REPEAT"
		elif check_check.search(inputStr) != None:
			self.Intent = "CHECK_ORDER"

		if self.Intent is None:
			hello_regex = re.compile("(hello|hey|how's it going|greetings|hi|yo)")

			hello = hello_regex.search(inputStr)

			if hello is not None:
				self.Intent = "HELLO"

		return self.Intent, inputStr


invalue = 'nomorepizzaplease'

for line in sys.stdin:
	invalue = line
	NLU = NLUDefault()
	print(NLU.parse(invalue))



