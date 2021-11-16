import pickle

pc = open("updateList.pickle","wb")
pickle.dump({},pc)
pc.close()
