import numpy as np
import matplotlib.pyplot as plt
votes=[747, 20, 781, 622]           
candidates=['best effort', 'entropy', 'nearest', 'threshold']  
x=np.arange(len(candidates))                     
plt.bar(x, votes, tick_label=candidates)     
plt.title('handoff')          
plt.xlabel('algorithm')  
plt.yticks(np.arange(0, 800, 100))                            
plt.ylabel('times')                          
plt.show()