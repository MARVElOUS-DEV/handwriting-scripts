import copy
import argparse
import enum

Field_Type = enum.Enum('Field_type', ('int','double','json','text','textarea','code', 'image', 'audio', 'video', 'stream', 'text_select', 'image_select','audio_select','video_select','capture'))

class Model():
  name = 'demo'
  field = 'CV'
  version= 'v20221001'
  label = 'demo'
  description = 'demo'

  def __init__(self, name):
    self.name = name
    return
  def run(self):
    kwargs=self.init_args()
    print('kwargs:',kwargs)
    self.load_model(kwargs)

    result = self.inference(**kwargs)

    print('result:', result)

  def load_model(self, save_path=None, **kwargs):
    print('load model ...', kwargs)
  def inference(self, **kwargs):
    print('inference ...', kwargs)
    return 'result'
  def init_args(self):
    main_parser = argparse.ArgumentParser(prog='ddddocr python exec')
    task_type_subparsers = main_parser.add_subparsers(title="启动类型", dest="task_type")
    inference_parser = task_type_subparsers.add_parser("inference", help="启动推理")

    inference_parser.add_argument("--img_file_path", type=str, help="OCR要识别的图片地址", default=None)
    input = vars(main_parser.parse_args())
    task_type = input.get('task_type', 'inference')
    if task_type != 'inference':
      raise "当前必须使用 inference 启动"
    kwargs = copy.deepcopy(input)
    if 'task_type' in kwargs:
      del kwargs['task_type']
    return kwargs
