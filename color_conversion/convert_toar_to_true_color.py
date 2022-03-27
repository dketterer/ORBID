import argparse
import glob
import logging
import os

import numpy as np
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrueColorConverter:
    def __init__(self, numpy_file=''):
        self.scale = 10000

        # channel order: value, red, green, blue
        color_curve = np.load(numpy_file)
        color_curve = (color_curve * self.scale).astype(np.uint16)
        self.color_curve = np.empty((4, self.scale), dtype=np.uint16)
        for channel in range(4):
            lut = np.interp(np.linspace(0, 255, self.scale), np.arange(255), color_curve[channel, ...]).astype(np.uint16)
            self.color_curve[channel, ...] = lut

    def apply_color_curve(self, source):
        target = np.ma.empty_like(source)
        _source = np.ma.array(source * self.scale, mask=source.mask).astype(np.uint16)

        # per channel
        for channel in range(source.shape[0]):
            intermediate = self.color_curve[channel + 1, ...][_source[channel, ...]]
            target[channel, ...] = self.color_curve[0, ...][intermediate]
        result = target / self.scale
        return result

    def process(self, source_path, target_path):
        s_arr = np.load(source_path)
        source = np.ma.masked_where(s_arr == 0, s_arr).astype('float64')

        source /= self.scale

        result = (self.apply_color_curve(source) * 255.).astype(np.uint8)
        # channels last
        np_8bit_img = np.swapaxes(result, 0, 2)
        # from (w, h, c) to (h, w, c) for open cv
        np_8bit_img = np.swapaxes(np_8bit_img, 0, 1)
        # change to bgr for opencv
        np_8bit_img = cv2.cvtColor(np_8bit_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(target_path, np_8bit_img)

    def process_all(self, indir, outdir):
        for tif_path in glob.glob(f'{indir}/*.npy'):
            file_name = os.path.basename(tif_path)

            name = file_name.removesuffix('.npy')
            target_path = os.path.join(outdir, f'{name}_TrueColor.png')

            logger.info("Processing %s", tif_path)
            self.process(tif_path, target_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('indir')
    parser.add_argument('outdir')
    parser.add_argument('color_curve')
    args = parser.parse_args()


    os.makedirs(args.outdir, exist_ok=True)

    tc = TrueColorConverter(args.color_curve)
    tc.process_all(args.indir, args.outdir)
