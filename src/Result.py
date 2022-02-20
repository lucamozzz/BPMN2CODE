from multiprocessing import Process

class Result:

	def runInParallel(*fns):
		proc = []
		for fn in fns:
			p = Process(target=fn)
			p.start()
			proc.append(p)
		for p in proc:
			p.join()


if __name__ == '__main__':
		set_steps(10)
		while steps > 0: 
 			check_distance
			if distance > 30: 
				runInParallel(turn_on_led, go_forward(20, distance))
				turn_off_led
				decrease_steps(1)
			else: 
 				decide_turn
				if decision == 'left': 
					turn_left
				else: 
 					turn_right




