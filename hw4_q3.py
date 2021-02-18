import re
import sys
from hw4_q1 import NLUDefault
import hw4_q2
from sklearn.metrics import f1_score


if __name__ == "__main__":

	def process_input(in_value):
		intent_val, trash = hw4_q2.convert_to_ngrams(["BOS "+in_value+" EOS"])
		intent_val = hw4_q2.feat_vector(intent_val[0], unique_ngrams)

		slots_val = hw4_q2.sent2features([(w,) for w in in_value.split()])

		intent = NLU_q2_intents.predict([intent_val])
		slots = NLU_q2_slots.predict([slots_val])

		annotated_utterance = hw4_q2.BIO2sent(in_value.split(), slots[0])

		return intent[0], annotated_utterance

	NLU_q1 = NLUDefault()
	NLU_q2_intents, NLU_q2_slots, unique_ngrams = hw4_q2.train_both_models()

	hw4_q2.evaluate_stats(NLU_q2_intents, NLU_q2_slots, 'eval_data.txt', unique_ngrams)

	with open('clean_eval.txt') as q1_data:
		sentences = q1_data.readlines()


	q1_predictions = [NLU_q1.parse(sentence) for sentence in sentences]
	#[(intent, annotated),]

	intents_preds = [l[0] for l in q1_predictions]
	slots_preds = [l[1] for l in q1_predictions]

	hw4_q2.evaluate_rules('eval_data.txt', intents_preds, slots_preds)


	with open("rules_preds.txt", "w") as output:
		for pair in q1_predictions:
			output.write("{}\t{}\n".format(pair[0], pair[1]))



	"""gold_intent = []
	gold_slots_BIO = []
	gold_slots_reg = []
	with open('eval_data.txt') as eval_data:
		for line in eval_data:
			gold_intent.append(line.strip().split("\t")[0])
			gold_slots_reg.append(line.strip().split("\t")[1])
			gold_slots_BIO.append([bio for (w, bio) in hw4_q2.sent2BIO(line.strip().split("\t")[1])])

	q1_eval_intents = []
	q1_eval_slots = []
	q2_eval_intents = []
	q2_eval_slots = []

	with open('q1_predictions.txt', 'w') as q1:
		with open('q2_predictions.txt', 'w') as q2:
			for line in sys.stdin:
				invalue = line.strip()

				intent_q1, slots_q1 = NLU_q1.parse(invalue) # q1 output
				intent_q2, slots_q2 = process_input(invalue) # q2 output

				q1_eval_intents.append(intent_q1)
				q1_eval_slots.append(slots_q1)

				q2_eval_intents.append(intent_q2)
				q2_eval_slots.append(slots_q2)

				q1.write("{}\t{}\n".format(intent_q1, slots_q1))
				q2.write(intent_slots_q2)

	print("q1 intents f1score" + str(f1_score(q1_eval_intents, gold_intent)))
	print("q2 intents f1score" + str(f1_score(q2_eval_intents, gold_intent)))

	q1_slot_acc = 0
	q2_slot_acc = 0

	for q1guess, q2guess in q1_eval_slots, q2_eval_slots:
		if q1guess == gold_slots_reg:
			q1_slot_acc += 1
		if q2guess == gold_slots_BIO:
			q2_slot_acc += 1

	q1_slot_acc = q1_slot_acc/len(q1_eval_slots)
	q2_slot_acc = q2_slot_acc/len(q2_eval_slots)

	print("q1 slot acc" + str(q1_slot_acc))
	print("q2 slot acc" + str(q2_slot_acc))"""



