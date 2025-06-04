class video_logger:
    def __init__(self,video_cfg) -> None:
        self.video_cfg = video_cfg
        self.frames = []

    def reset(self):
        self.frames.clear()

    def read_single_frame(self,frame):
        self.frames.append(frame)

    def save_video(self,iter,log_dir):
        print("saved!")
        path = log_dir + "/videos/{:05d}".format(iter)
        save_video(self.frames,path, fps=1 / self.video_cfg.env_dt)

    def is_complete(self):
        complete = False
        if len(self.frames) >= (self.video_cfg.video_length_in_sec//self.video_cfg.env_dt):
            complete=True
        return complete

def pJoin(*args):
    from os.path import join
    args = [a for a in args if a]
    if args:
        return join(*args)
    return None

def save_video(frame_stack, path, format=None, fps=20, **imageio_kwargs):
    """
    Let's do the compression here. Video frames are first written to a temporary file
    and the file containing the compressed data is sent over as a file buffer.

    Save a stack of images to

    :param frame_stack: the stack of video frames
    :param key: the file key to which the video is logged.
    :param format: Supports 'mp4', 'gif', 'apng' etc.
    :param imageio_kwargs: (map) optional keyword arguments for `imageio.mimsave`.
    :return:
    """
    format = "mp4"
    path += "." + format
    import tempfile, imageio  # , logging as py_logging
    # py_logging.getLogger("imageio").setLevel(py_logging.WARNING)
    with tempfile.NamedTemporaryFile(suffix=f'.{format}') as ntp:
        from skimage import img_as_ubyte
        try:
            imageio.mimsave(path, img_as_ubyte(frame_stack), format=format, fps=fps, **imageio_kwargs)
        except imageio.core.NeedDownloadError:
            imageio.plugins.ffmpeg.download()
            imageio.mimsave(path, img_as_ubyte(frame_stack), format=format, fps=fps, **imageio_kwargs)
        ntp.seek(0)
