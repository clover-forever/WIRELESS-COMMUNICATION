import numpy as np
import matplotlib.pyplot as plt
votes=[6352, 166, 6641, 5225]           
candidates=['best effort', 'entropy', 'nearest', 'threshold']  
x=np.arange(len(candidates))                     
plt.bar(x, votes, tick_label=candidates)     
plt.title('handoff')          
plt.xlabel('algorithm')  
plt.yticks(np.arange(0, 7000, 500))                            
plt.ylabel('times')                          
plt.show()
