import tensorflow.compat.v1 as tf

class BeautyGan:
    def __init__(self):
        with tf.Graph().as_default():
            output_graph_def = tf.GraphDef()
            with open("model/BeautyGAN.pb", "rb") as f:
                output_graph_def.ParseFromString(f.read())
                tf.import_graph_def(output_graph_def, name="")
            self.sess = tf.Session()
            self.X = self.sess.graph.get_tensor_by_name('X:0')
            self.Y = self.sess.graph.get_tensor_by_name('Y:0')
            self.Xs = self.sess.graph.get_tensor_by_name('generator/xs:0')
    def predict(self, no_makeup, makeup):
        X_img = self.preprocess(no_makeup)
        Y_img = self.deprocess(makeup)
        output = self.sess.run(self.Xs, feed_dict={self.X: [X_img], self.Y: [Y_img]})
        output = (output + 1) / 2
        return output
    def preprocess(self, img):
        return (img / 255. - 0.5) * 2
    def deprocess(self, img):
        return (img + 1) / 2