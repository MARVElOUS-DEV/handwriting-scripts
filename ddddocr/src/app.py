import os
from model_pkg.model import Model 
import ddddocr
import cv2

class App(Model):
  name='ddddocr'
  label='验证码识别'
  describe="ai识别验证码文字和验证码目标"
  field="机器视觉"
  scenes="图像识别"
  status='online'
  version='v20221001'
  def load_model(self,save_model_dir=None,**kwargs):
    # 模型
    self.ocr = ddddocr.DdddOcr(beta=True)
    self.dec = ddddocr.DdddOcr(det=True)
  def inference(self,img_file_path):
    # 验证码图片
    if not os.path.exists(img_file_path):  # 检查最终路径是否在预期的上传目录中
        raise IOError()
    with open(img_file_path, 'rb') as f:
        image = f.read()
        print(type(image))

    # 目标检测
    poses = self.dec.detection(image)
    print(poses)

    result_im = cv2.imread(img_file_path)

    # 遍历检测出的文字
    result_text=''
    for box in poses:
        x1, y1, x2, y2 = box
        cropped = result_im[y1:y2, x1:x2]
        cv2.imwrite("temp.jpg", cropped)
        txt = self.ocr.classification(open('temp.jpg', 'rb').read())
        result_text+=txt
        # 给每个文字画矩形框
        result_im = cv2.rectangle(result_im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
    if os.path.exists('temp.jpg'):
        os.remove('temp.jpg')

    os.makedirs('result', exist_ok=True)
    save_path = os.path.join('result', os.path.basename(img_file_path))
    cv2.imwrite(save_path, result_im)
    back=[{
        "image":save_path,
        "text":result_text
    }]
    return back

if __name__ == "__main__":
  # python app.py inference --img_file_path xx 
  model=App('test')
  model.run()
