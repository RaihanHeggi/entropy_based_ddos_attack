# Entropy Based DDoS Attack Detection on SDN Network

Workflow 
1. Preprocessing Data For Feature Selection 
2. Testing Dataset with ML-Classifier (ANN, Decision Tree)
3. Develop Entropy Based Classification Model
4. Develop Markov Chain based Classification Model
5. Integration with SDN Network



To User this Code You Will Need Some Library Such As
1. Pandas
2. Matplotlib 
3. Seaborn
4. Numpy 
5. Sklearn
6. Scipy

**Update For Now Currently working on entropy-based-model that model can reach accuracy up-to 69% still need to adjust hyperparameters**


Image of Running Testing Using (Bytes, Packetcount, and Protocol Parameters)
![image](https://user-images.githubusercontent.com/58820833/143678576-b53354e9-a36a-46c8-9e89-7ab45f4f80cd.png)


how to running ryu controller 
sudo ryu-manager --observe-links ryu/app/simple_switch_13.py ryu/app/gui_topology/gui_topology.py simple_monitor_detect.py

