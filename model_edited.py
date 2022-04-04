from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.models import Sequential

def create_model():

    model=Sequential()
    model.add(Dense(24,activation="relu",input_shape=(24,)))
    model.add(Dense(24,activation="relu"))
    #色々modelの構造をいじってみて実験すると良い。下のコメントを外すだけでもまた形状が変化する。
    #model.add(Dense(64,activation="relu"))
    model.add(Dense(1))

    return model
