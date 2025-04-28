import tkinter as tk
from tkinter import simpledialog
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

##########################
# 1) HandCanvas Class
##########################
class HandCanvas(tk.Frame):
    def __init__(self, master, image_path, scale=0.5):
        super().__init__(master, bg="#2c3e50")
        pil_image = Image.open(image_path)
        orig_w, orig_h = pil_image.size
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        pil_image = pil_image.resize((new_w, new_h), Image.LANCZOS)
        self.hand_image = ImageTk.PhotoImage(pil_image)
        self.canvas = tk.Canvas(self, width=new_w, height=new_h, bd=0, highlightthickness=0, bg="#ecf0f1")
        self.canvas.pack(padx=5, pady=5)
        self.canvas.create_image(0, 0, anchor="nw", image=self.hand_image)
        
        if "left" in image_path.lower():
            self.finger_regions = {
                "pinky_top": self.canvas.create_oval(0, 55, 25, 75, fill="", outline="", width=0),
                "ring_top": self.canvas.create_oval(25, 17, 55, 40, fill="", outline="", width=0),
                "middle_top": self.canvas.create_oval(55, 5, 85, 30, fill="", outline="", width=0),
                "index_top": self.canvas.create_oval(130, 20, 100, 40, fill="", outline="", width=0)
            }
        elif "right" in image_path.lower():
            self.finger_regions = {
                "pinky_top": self.canvas.create_oval(175, 60, 202, 80, fill="", outline="", width=0),
                "ring_top": self.canvas.create_oval(145, 20, 173, 40, fill="", outline="", width=0),
                "middle_top": self.canvas.create_oval(115, 7, 143, 30, fill="", outline="", width=0),
                "index_top": self.canvas.create_oval(75, 20, 100, 40, fill="", outline="", width=0),
                "thumb": self.canvas.create_oval(20, 125, 40, 145, fill="", outline="", width=0)
            }
        else:
            self.finger_regions = {
                "index_top": self.canvas.create_polygon(100, 20, 120, 20, 120, 40, 100, 40,
                                                        fill="", outline="", width=0),
                "middle_top": self.canvas.create_polygon(140, 20, 160, 20, 160, 40, 140, 40,
                                                         fill="", outline="", width=0)
            }
    
    def highlight_finger(self, finger_key, color="green"):
        if finger_key in self.finger_regions:
            self.canvas.itemconfig(self.finger_regions[finger_key], fill=color)
    
    def clear_highlights(self):
        for key in self.finger_regions:
            self.canvas.itemconfig(self.finger_regions[key], fill="")

##########################
# 2) Main TypingSpeedApp (Design updates added)
##########################
class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test with Finger Guidance")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#2c3e50")
        
        # NEW: For cumulative time, set a session start time (never reset)
        self.lesson_start_time = None
        self.last_key_time = None

        self.test_finished = False
        self.analysis_shown = False
        self.history = []
        
        self.lessons = {
            "Lesson 1": {
                "Lesson 1.1(home row)": (
                    "aa ss dd ff jj kk ll ;;\n"
                    "as as df df jk jk l; l;\n"
                ),
                "exercise 1": ("ad ad jk jk ad ad jk jk\n"
                               "sf sf k; k; sf sf k; k;\n"
                               "adad jkjk adad jkjk\n"
                               "sfsf k;k; sfsf k;k;\n"
                               "afaf j;j; afaf j;j;\n"
                               "sdsd klkl sdsd klkl\n"
                               "j;j; afaf j;j; afaf\n"
                ),
                "exercise 2": ("add add add add\n"
                               "ads ads ads ads\n"
                               "dad dad dad dad\n"
                               "ask ask ask ask\n"
                               "fad fad fad fad\n"
                               "all all all all\n"
                               "daff daff daff daff\n"
                ),
                "exercise 3": ("ad ad jk jk ad ad jk jk\n"
                               "sf sf k; k; sf sf k; k;\n"
                               "adad jkjk adad jkjk\n"
                               "sfsf k;k; sfsf k;k;\n"
                               "afaf j;j; afaf j;j;\n"
                               "sdsd klkl sdsd klkl\n"
                               "j;j; afaf j;j; afaf\n"
                )
            },
            "Lesson 2": {
                "Lesson 2.1(e and i)": (
                    "ee ii ee ii\n"
                    "ei ei ie ie\n"
                    "fefe fefe efef efef\n"
                    "jiji jiji ijij ijij\n"
                    "defe defe kiji kiji\n"
                    "sede sede liki liki\n"
                ),
                "exercise 1": ("aeil aeil siek siek\n"
                               "iles iles jsie jsie\n"
                               "jski jski lesj lesj\n"
                               "ejej ejej sife sife\n"
                               "aile aile skie skie\n"
                               "deji deji eaia eaia\n"
                               "jisi jisi kesi kesi\n"
                ),
                "exercise 2": ("ejlk ejlk deji deji\n"
                               "jlki jlki dije dije\n"
                               "flik flik difi difi\n"
                               "seie seie skjd skjd\n"
                               "alji alji sdej sdej\n"
                               "jifd jifd feas feas\n"
                               "keid keid side side\n"
                )
            },
            "Lesson 3": {
                "Lesson 3.1(r and u)": (
                    "rr uu rr uu\n"
                    "ru ru ur ur\n"
                    "drfr drfr juku juku\n"
                    "rfrd rfrd ujuk ujuk\n"
                    "druk druk jurf jurf\n"
                    "erui erui iure iure\n"
                ),
                "exercise 1": ("aeil aeil siek siek\n"
                               "iles iles jsie jsie\n"
                               "jski jski lesj lesj\n"
                               "ejej ejej sife sife\n"
                               "aile aile skie skie\n"
                               "deji deji eaia eaia\n"
                               "jisi jisi kesi kesi\n"
                ),
                "exercise 2": ("ejlk ejlk deji deji\n"
                               "jlki jlki dije dije\n"
                               "flik flik difi difi\n"
                               "seie seie skjd skjd\n"
                               "alji alji sdej sdej\n"
                               "jifd jifd feas feas\n"
                               "keid keid side side\n"
                )
            },
            "Lesson 4": {
                "Lesson 4.1(w and o)": (
                    "ww oo ww oo\n"
                    "wo wo ow ow\n"
                    "rfww rfww eokr eokr\n"
                    "iooe iooe okes okes\n"
                    "ofrw ofrw orws orws\n"
                    "swkj swkj aorf aorf\n"
                ),
                "exercise 1": ("fwdl fwdl edwl edwl\n"
                               "orro orro wesw wesw\n"
                               "euwe euwe oidj oidj\n"
                               "froi froi odko odko\n"
                               "ioso ioso lwdu lwdu\n"
                               "lrlo lrlo ossi ossi\n"
                               "iujw iujw jlkw jlkw\n"
                )
            },
            "Lesson 5": {
                "Lesson 5.1(c and n)": (
                    "cc nn cc nn\n"
                    "cn cn nc nc\n"
                    "ncsf ncsf lncf lncf\n"
                    "caou caou ckcf ckcf\n"
                    "snno snno lnok lnok\n"
                    "ucne ucne ucrf ucrf\n"
                ),
                "exercise 1": ("acci acci winu winu\n"
                               "uncr uncr ndin ndin\n"
                               "rcis rcis cwcu cwcu\n"
                               "knie knie lcse lcse\n"
                               "awcr awcr ccan ccan\n"
                               "flce flce dsnw dsnw\n"
                               "ronr ronr aene aene\n"
                )
            },
            "Lesson 6": {
                "Lesson 6.1(, and .)": (
                    ",, .. ,, ..\n"
                    ",. ,. ., .,\n"
                    "wc.c wc.c la,c la,c\n"
                    ".esk .esk kd,r kd,r\n"
                    "el.e el.e .sdj .sdj\n"
                    "sru. sru. f,,n f,,n\n"
                ),
                "exercise 1": ("lfn. lfn. u,ku u,ku\n"
                               "lsn, lsn, u,ef u,ef\n"
                               "er.r er.r d,of d,of\n"
                               ",saw ,saw oa,d oa,d\n"
                               "o,,s o,,s ...k ...k\n"
                               ".dsi .dsi u,ea u,ea\n"
                               "ee,n ee,n w,,k w,,k\n"
                )
            },
             "Lesson 7": {
                "Lesson 7.1(Capital letters)": (
                    "AA SS DD FF\n"
                    "JJ KK LL EE\n"
                    "II RR UU WW\n"
                    "OO CC NN\n"
                    "fUFU fUFU RjdL RjdL\n"
                    "kWNN kWNN OJFS OJFS\n"
                ),
                "exercise 1": ("EEEc EEEc rUiC rUiC\n"
                               "fLDa fLDa IkLC IkLC\n"
                               "EIRo EIRo AKRE AKRE\n"
                               "rNsD rNsD UNFS UNFS\n"
                               "UFLO UFLO iFJN iFJN\n"
                               "jDKJ jDKJ KWjw KWjw\n"
                               "UNlU UNlU UIOi UIOi\n"
                ),
                "exercise 2": ("wrRk UOfe CnwE aEoF\n"
                               "SoSl j.;n oirc .Knl\n"
                               ",NKs SUue ,IEw klw,\n"
                               "rnwe LDWs iosS KudK\n"
                               "uiKJ dsfE nEIN I.sr\n"
                               "ndIU F;CK fnIc OIrA\n"
                               "fKfA Jnok a.sc iLiu\n"
                )
            },
            "Lesson 8": {
                "Lesson 8.1(v and m)": (
                    "vv mm vv mm\n"
                    "vm vm mv mv\n"
                    "cnlv cnlv vuic vuic\n"
                    "cnlv cnlv vuic vuic\n"
                    "asmu asmu dvce dvce\n"
                    "vuns vuns mvfn mvfn\n"
                ),
                "exercise 1": ("mjld mjld uumo uumo\n"
                               "vvri vvri advo advo\n"
                               "dvls dvls umsn umsn\n"
                               "devo devo afkv afkv\n"
                               "mfdm mfdm mnlv mnlv\n"
                               "mrsn mrsn usnm usnm\n"
                               "wvrd wvrd ovrw ovrw\n"
                )
            },
             "Lesson 9": {
                "Lesson 9.1( t and y)": (
                    "tt yy tt yy\n"
                    "ty ty yt yt\n"
                    "yand yand tlvt tlvt\n"
                    "ajtj ajtj fatt fatt\n"
                    "yymn yymn jtlo jtlo\n"
                    "llts llts tyvl tyvl\n"
                ),
                "exercise 1": ("utoc utoc wtiy wtiy\n"
                               "utey utey votv votv\n"
                               "fomy fomy tmuu tmuu\n"
                               "jtyr jtyr ldct ldct\n"
                               "fnjt fnjt ymyn ymyn\n"
                               "ayke ayke yfev yfev\n"
                               "totm totm mjyv mjyv\n"
                )
            },
            "Lesson 10": {
                "Lesson 10.1(g, h, ' and \")": (
                    "gg hh '' "" gg hh '' " "\n"
                    "gh'\" gh' \" \" 'hg \" 'hg\n"
                    "yjho yjho s'g\" s'g\"\n"
                    "jgc\" jgc\" k'sh k'sh\n"
                    "ig'y ig'y gnhw gnhw\n"
                    "vgcf vgcf kvh' kvh'\n"
                ),
                "exercise 1": ("ohho ohho n\"hg n\"hg\n"
                               "gjve gjve nhf\" nhf\"\n"
                               "fngf fngf htgy htgy\n"
                               "u'wf u'wf aomh aomh\n"
                               "ihnv ihnv rjgf rjgf\n"
                               "uokg uokg r'oy r'oy\n"
                               "lfht lfht awhk awhk\n"
                )
            },
            "Lesson 11": {
                "Lesson 11.1(q and p)": (
                    "qq pp qq pp\n"
                    "qp qp pq pq\n"
                    "hpoi hpoi qcvs qcvs\n"
                    "npjq npjq yerq yerq\n"
                    "cppp cppp phgn phgn\n"
                    "thpl thpl wqnw wqnw\n"
                ),
                "exercise 1": ("lvqw lvqw pdpu pdpu\n"
                               "pwqv pwqv lncq lncq\n"
                               "qrvk qrvk oqsc oqsc\n"
                               "tqdi tqdi oqtm oqtm\n"
                               "odqp odqp shpt shpt\n"
                               "ypyj ypyj sqko sqko\n"
                               "tqrt tqrt doqg doqg\n"
                )
            },
            "Lesson 12": {
                "Lesson 12.1(x and b)": (
                    "xx bb xx bb\n"
                    "xb xb bx bx\n"
                    "usxm usxm abab abab\n"
                    "cxek cxek nxwn nxwn\n"
                    "xxbt xxbt jbsn jbsn\n"
                    "gexx gexx adbv adbv\n"
                ),
                "exercise 1": ("ixqm ixqm lixr lixr\n"
                               "kqbn kqbn jbgd jbgd\n"
                               "llbv llbv vrkb vrkb\n"
                               "uxqt uxqt obbn obbn\n"
                               "fubn fubn txgt txgt\n"
                               "xugt xugt vbby vbby\n"
                               "vhxy vhxy sibn sibn\n"
                )
            },
             "Lesson 13": {
                "Lesson 13.1( z, ?, :, <, > and /)": (
                    "zz ?? :: << // >>\n"
                    "z? z< z/ >z :z\n"
                    "zzsl zzsl ha?l ha?l\n"
                    "tszy tszy atza atza\n"
                    "?hze ?hze itd? itd?\n"
                    "z?wd z?wd l?un l?un\n"
                ),
                "exercise 1": ("r?rh r?rh biaz biaz\n"
                               "ke?b ke?b fzjy fzjy\n"
                               "de?z de?z mc?z mc?z\n"
                               "lzzv lzzv x/za x/za\n"
                               "ub?k ub?k vzzg vzzg\n"
                               "gfo? gfo? zvgl zvgl\n"
                               "sxzt sxzt j?hw j?hw\n"
                ),
                "exercise 2": ("WHpZ E/?P ,rgl :z>R\n"
                               "zVxj JZNc K:V? Wd?Y\n"
                               "cz>Z X.lX <>:n tmz/\n"
                               ";>LV \"Dok wyIL <or<\n"
                               "cn:R j,zI bWzQ <z/X\n"
                               "/St: zZfF Zz/M ZA>n\n"
                               "KY?R H;:? VcfN OXVU\n"
                )
            },
            "Lesson 14": {
                "Lesson 14.1(Numbers)": (
                    "13579 13579 24680 24680\n"
                    "28160 28160 73594 73594\n"
                    "nn26 nn26 5ypa 5ypa\n"
                    "op5e op5e 22oi 22oi\n"
                    "h8wm h8wm 71fx 71fx\n"
                    "q2wg q2wg hub2 hub2\n"
                ),
                "exercise 1": ("a7w9 a7w9 v46t v46t\n"
                               "d0hk d0hk opp6 opp6\n"
                               "ve57 ve57 u49c u49c\n"
                               "7n2h 7n2h 7x2a 7x2a\n"
                               "80z9 80z9 5l4k 5l4k\n"
                               "x7ic x7ic hk1c hk1c\n"
                               "l4e0 l4e0 8370 8370\n"
                ),
                "exercise 2": ("btS8 BL.4 M597 4Ex<\n"
                               "iuKU 0U:R KvZ4 jUaO\n"
                               "3.d1 CO'8 0eQX xwS8\n"
                               "D92D FnQb S0jA C:1n\n"
                               "O849 o3QI hu3M 9c4q\n"
                               "4M3B Qn92 :I<S vlRq\n"
                               "qr99 4.k0 ?p;I I4Yr\n"
                )
            },
            "Lesson 15": {
                "Lesson 15.1(All keys)": (
                    "+}+} +}+} $h%f $h%f\n"
                    "#3#^ #3#^ `\=< `\=<\n"
                    "qrk/ qrk/ e^_q e^_q\n"
                    "[j{3 [j{3 x2^+ x2^+\n"
                    "3_=% 3_=% i{y\" i{y\"\n"
                    "-$uc -$uc ^!gv ^!gv\n"
                ),
                "exercise 1": ("6\8\ 6\8\ ~#$# ~#$#\n"
                               "#bg| #bg| rpd rpd\n"
                               "#x@| #x@| t+~_ t+~_\n"
                               "]|>< ]|>< j{#- j{#-\n"
                               "x%3i x%3i /vno /vno\n"
                               "5w/v 5w/v &:ya &:ya\n"
                               "|f3 |f3 #{ #{\n"
                )
            },
            
            "Full Text": " The quick brown fox jumps over the lazy dog."
        }
        self.current_lesson = "Full Text"
        self.target_text = self.lessons[self.current_lesson]
        
        # For multi-line lessons.
        self.lesson_lines = None  
        self.current_line_index = 0
        
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Top Control Frame
        control_frame = tk.Frame(root, bg="#34495e")
        control_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        lesson_frame = tk.Frame(control_frame, bg="#34495e")
        lesson_frame.pack(side=tk.LEFT, padx=10)
        
        lesson_label = tk.Label(lesson_frame, text="Select Lesson:", font=("Helvetica", 16), bg="#34495e", fg="white")
        lesson_label.pack(side=tk.LEFT, padx=(0,5))
        
        self.main_lesson_var = tk.StringVar(value="Select Main Lesson")
        self.main_lesson_menu = tk.OptionMenu(lesson_frame, self.main_lesson_var, *self.lessons.keys(), command=self.update_sub_lessons)
        self.main_lesson_menu.config(font=("Helvetica", 16), bg="#ecf0f1")
        self.main_lesson_menu.pack(side=tk.LEFT, padx=5)
        
        self.sub_lesson_var = tk.StringVar(value="Select Sub Lesson")
        self.sub_lesson_menu = tk.OptionMenu(lesson_frame, self.sub_lesson_var, "")
        self.sub_lesson_menu.config(font=("Helvetica", 16), bg="#ecf0f1")
        self.sub_lesson_menu.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(lesson_frame, text="Load Lesson", font=("Helvetica", 16), command=self.load_selected_lesson,
                             bg="#3498db", fg="white", relief="flat", padx=10, pady=5)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        custom_btn = tk.Button(lesson_frame, text="Custom Text", font=("Helvetica", 16), command=self.custom_text,
                               bg="#3498db", fg="white", relief="flat", padx=10, pady=5)
        custom_btn.pack(side=tk.LEFT, padx=5)
        
        exit_button = tk.Button(control_frame, text="Exit", font=("Helvetica", 16),
                                command=self.root.destroy, bg="#e74c3c", fg="white", relief="flat", padx=10, pady=5)
        exit_button.pack(side=tk.RIGHT)
        
        # Info frame (target display, stats, clock)
        info_frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief="groove")
        info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=10)
        
        self.target_display = tk.Text(info_frame, font=("Helvetica", 20), height=3,
                                      wrap="word", state="disabled", bg="white", bd=0)
        self.target_display.pack(side=tk.TOP, fill=tk.X, pady=(5,5), padx=5)
        self.target_display.config(state="normal")
        self.target_display.insert("1.0", self.target_text)
        self.target_display.config(state="disabled")
        self.target_display.tag_config("right", background="#2ecc71")
        self.target_display.tag_config("wrong", background="#e74c3c")
        
        stats_frame = tk.Frame(info_frame, bg="#ecf0f1")
        stats_frame.pack(side=tk.TOP, anchor="w", pady=(5,5), padx=5)
        self.speed_label = tk.Label(stats_frame, text="Speed: 0.0 WPM", font=("Helvetica", 16), bg="#ecf0f1")
        self.speed_label.pack(side=tk.LEFT, padx=(0,20))
        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 100.0%", font=("Helvetica", 16), bg="#ecf0f1")
        self.accuracy_label.pack(side=tk.LEFT, padx=(0,20))
        self.error_label = tk.Label(stats_frame, text="Error: 0", font=("Helvetica", 16), bg="#ecf0f1")
        self.error_label.pack(side=tk.LEFT, padx=(0,20))
        self.time_label = tk.Label(stats_frame, text="Time: 0.0 s", font=("Helvetica", 16), bg="#ecf0f1")
        self.time_label.pack(side=tk.LEFT)
        
        # Text area (user input) with modern styling
        text_frame = tk.Frame(root, bg="#ecf0f1")
        text_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        self.text_area = tk.Text(text_frame, font=("Helvetica", 24), wrap="word", bg="white", bd=2, relief="flat")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_area.focus_set()
        self.text_area.bind("<Key>", self.on_key_press)
        
        # Hands and keyboard frame
        hands_keyboard_frame = tk.Frame(root, bg="#2c3e50")
        hands_keyboard_frame.grid(row=3, column=0, pady=10, padx=15, sticky="ew")
        hands_keyboard_frame.columnconfigure(0, weight=1)
        hands_keyboard_frame.columnconfigure(1, weight=2)
        hands_keyboard_frame.columnconfigure(2, weight=1)
        
        self.left_hand = HandCanvas(hands_keyboard_frame, "speed_typing\\23002170110076_Python\\left.png", scale=0.3)
        self.left_hand.grid(row=0, column=0, sticky="s", padx=5)
        
        keyboard_frame = tk.Frame(hands_keyboard_frame, bg="#2c3e50")
        keyboard_frame.grid(row=0, column=1, padx=10)
        self.key_buttons = {}
        keyboard_layout = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Back"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
            ["Space"]
        ]
        indent_values = [0, 25, 50, 75, 0]
        for i, row_keys in enumerate(keyboard_layout):
            row_frame = tk.Frame(keyboard_frame, bg="#2c3e50")
            row_frame.pack(side=tk.TOP, anchor="center", pady=3)
            if indent_values[i] > 0:
                spacer = tk.Frame(row_frame, width=indent_values[i], height=1, bg="#2c3e50")
                spacer.pack_propagate(False)
                spacer.pack(side=tk.LEFT)
            for j, key in enumerate(row_keys):
                btn_width = 40 if key == "Space" else 7 if key in ["Tab", "Back", "CapsLock", "Enter", "Shift"] else 5
                btn = tk.Button(row_frame, text=key, font=("Helvetica", 16),
                                width=btn_width, height=2, relief="flat", bg="#bdc3c7", fg="black")
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                btn.original_bg = btn.cget("background")
                if key == "Shift" and i == 3:
                    if j == 0:
                        btn.shift_side = "left"
                    elif j == len(row_keys) - 1:
                        btn.shift_side = "right"
                    else:
                        btn.shift_side = None
                self.key_buttons.setdefault(key, []).append(btn)
        
        self.right_hand = HandCanvas(hands_keyboard_frame, "speed_typing\\23002170110076_Python\\right.png", scale=0.3)
        self.right_hand.grid(row=0, column=2, sticky="s", padx=5)
        
        self.finger_mapping = {
            "G": ("left", "index_top"),
            "F": ("left", "index_top"),
            "D": ("left", "middle_top"),
            "S": ("left", "ring_top"),
            "A": ("left", "pinky_top"),
            "R": ("left", "index_top"),
            "T": ("left", "index_top"),
            "E": ("left", "middle_top"),
            "W": ("left", "ring_top"),
            "Q": ("left", "pinky_top"),
            "V": ("left", "index_top"),
            "B": ("left", "index_top"),
            "C": ("left", "middle_top"),
            "X": ("left", "ring_top"),
            "Z": ("left", "pinky_top"),
            "H": ("right", "index_top"),
            "J": ("right", "index_top"),
            "K": ("right", "middle_top"),
            "O": ("right", "ring_top"),
            ";": ("right", "pinky_top"),
            "U": ("right", "index_top"),
            "Y": ("right", "index_top"),
            "I": ("right", "middle_top"),
            "L": ("right", "ring_top"),
            "P": ("right", "pinky_top"),
            "N": ("right", "index_top"),
            "M": ("right", "index_top"),
            "<": ("right", "middle_top"),
            ">": ("right", "ring_top"),
            "?": ("right", "pinky_top"),
            "[": ("right", "ring_top"),
            "]": ("right", "pinky_top"),
            "\\": ("right", "pinky_top"),
            ":": ("right", "pinky_top"),
            "\"": ("right", "pinky_top"),
            ",": ("right", "middle_top"),
            ".": ("right", "ring_top"),
            "/": ("right", "pinky_top"),
            "`": ("left", "pinky_top"),
            "~": ("left", "pinky_top"),
            "!": ("left", "pinky_top"),
            "@": ("left", "ring_top"),
            "#": ("left", "middle_top"),
            "$": ("left", "index_top"),
            "%": ("left", "index_top"),
            "^": ("left", "middle_top"),
            "&": ("left", "ring_top"),
            "*": ("left", "pinky_top"),
            "(": ("right", "pinky_top"),
            ")": ("right", "pinky_top"),
            "_": ("right", "ring_top"),
            "+": ("right", "pinky_top"),
            "{": ("left", "pinky_top"),
            "}": ("right", "pinky_top"),
            "|": ("right", "pinky_top"),
            "Space":("right", "thumb")
        }
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        self.update_next_finger()
        self.update_clock()
    
    ###################################
    # Lesson & Custom Text Methods
    ###################################
    def update_sub_lessons(self, main_lesson):
        menu = self.sub_lesson_menu["menu"]
        menu.delete(0, "end")
        if isinstance(self.lessons.get(main_lesson), dict):
            sub_lessons = list(self.lessons[main_lesson].keys())
            self.sub_lesson_var.set(sub_lessons[0])
            for sub in sub_lessons:
                menu.add_command(label=sub, command=lambda s=sub: self.sub_lesson_var.set(s))
        else:
            self.sub_lesson_var.set("")
            menu.add_command(label="", command=lambda: None)
        self.reset_test()
    
    def load_selected_lesson(self):
        main = self.main_lesson_var.get()
        if isinstance(self.lessons.get(main), dict):
            sub = self.sub_lesson_var.get()
            self.target_text = self.lessons[main].get(sub, "")
            self.current_lesson = f"{main} - {sub}"
        else:
            self.target_text = self.lessons.get(main, "")
            self.current_lesson = main
        self.reset_test()
    
    def custom_text(self):
        custom = simpledialog.askstring("Custom Text", "Enter your custom text:")
        if custom:
            self.current_lesson = "Custom"
            self.target_text = custom
            self.reset_test()
    
    def reset_test(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", "end")
        self.lesson_start_time = None  
        self.last_key_time = None
        self.test_finished = False
        self.analysis_shown = False
        self.history = []
    
        self.total_chars_typed = 0  
        self.cumulative_correct_chars = 0  
        self.error_count = 0
    
        self.speed_label.config(text="Speed: 0.0 WPM")
        self.accuracy_label.config(text="Accuracy: 100.0%")
        self.error_label.config(text="Error: 0")
        self.time_label.config(text="Time: 0.0 s")
        
        if "\n" in self.target_text:
            self.lesson_lines = self.target_text.splitlines()
            self.current_line_index = 0
            current_line = self.lesson_lines[self.current_line_index]
        else:
            self.lesson_lines = None
            current_line = self.target_text
        self.target_display.config(state="normal")
        self.target_display.delete("1.0", "end")
        self.target_display.insert("1.0", current_line)
        self.target_display.config(state="disabled")
        
        self.text_area.focus_set()
        self.update_next_finger()
        self.update_clock()

    ###################################
    # Clock Update Method (cumulative)
    ###################################
    def update_clock(self):
        if self.test_finished:
            return
        if self.lesson_start_time is None:
            self.time_label.config(text="Time: 0.0 s")
        else:
            active_time = time.time() - self.lesson_start_time
            self.time_label.config(text=f"Time: {active_time:.1f} s")
        self.root.after(100, self.update_clock)

    ###################################
    # Key Handling & Finger Guidance
    ###################################
    def get_key_label(self, event):
        special_keys = {
            "BackSpace": "Back",
            "Tab": "Tab",
            "Return": "Enter",
            "Enter": "Enter",
            "Shift_L": "Shift",
            "Shift_R": "Shift",
            "Caps_Lock": "CapsLock"
        }
        if event.keysym in special_keys:
            return special_keys[event.keysym]
        symbol_mapping = {
            "!": "1", "@": "2", "#": "3", "$": "4", "%": "5",
            "^": "6", "&": "7", "*": "8", "(": "9", ")": "0",
            "_": "-", "+": "=", "{": "[", "}": "]", "|": "\\",
            ":": ";", '"': "'", "<": ",", ">": ".", "?": "/", "~": "`"
        }
        if event.char in symbol_mapping:
            return symbol_mapping[event.char]
        if event.char:
            if event.char == " ":
                return "Space"
            elif event.char.isalpha():
                return event.char.upper()
            else:
                return event.char
        return None

    def on_key_press(self, event):
        if self.test_finished:
            return
        now = time.time()
        if self.lesson_start_time is None:
            self.lesson_start_time = now
            self.last_key_time = now
        else:
            self.last_key_time = now
        self.root.after(1, self.update_stats)
        return

    def update_stats(self):
        current_text = self.text_area.get("1.0", "end-1c")
        elapsed_time = time.time() - self.lesson_start_time if self.lesson_start_time else 0
        effective_elapsed = elapsed_time if elapsed_time > 2 else 2
    
        if self.lesson_lines is not None:
            total_chars = self.total_chars_typed + len(current_text)
            wpm = (total_chars / 5) * (60 / effective_elapsed)
        else:
            wpm = (len(current_text) / 5) * (60 / effective_elapsed)
                
        self.speed_label.config(text=f"Speed: {wpm:.1f} WPM")
        
        if self.lesson_lines:
            target = self.lesson_lines[self.current_line_index]
            correct_current = sum(1 for i, ch in enumerate(current_text)
                                  if i < len(target) and ch == target[i])
            overall_correct = self.cumulative_correct_chars + correct_current
            overall_total = self.total_chars_typed + len(current_text)
            accuracy = (overall_correct / overall_total * 100) if overall_total > 0 else 100
        else:
            target = self.target_text
            correct_chars = sum(1 for i, ch in enumerate(current_text)
                                if i < len(target) and ch == target[i])
            accuracy = (correct_chars / len(current_text) * 100) if current_text else 100
    
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        if self.lesson_lines is not None:
            current_errors = len(current_text) - (overall_correct - self.cumulative_correct_chars)
            error_count = self.error_count + current_errors
        else:
            error_count = len(current_text) - correct_chars


        self.error_label.config(text=f"Error: {error_count}")

        self.final_elapsed_time = elapsed_time
        self.final_speed = wpm
        self.final_accuracy = accuracy
        self.final_errors = error_count
    
        self.history.append((elapsed_time, wpm, accuracy))
        self.update_content_highlights()
        
        if self.lesson_lines:
            if len(current_text.rstrip()) == len(target.rstrip()):
                self.root.after(100, self.progress_to_next_line)
        else:
            if len(current_text.rstrip()) == len(target.rstrip()):
                self.test_finished = True
                self.analysis_shown = True
                self.text_area.config(state="disabled")
                self.root.after(200, self.show_analysis)
        
        self.update_next_finger()

    def update_content_highlights(self):
        if self.lesson_lines:
            target = self.lesson_lines[self.current_line_index]
        else:
            target = self.target_text
        user_text = self.text_area.get("1.0", "end-1c")
        self.target_display.config(state="normal")
        self.target_display.tag_remove("right", "1.0", "end")
        self.target_display.tag_remove("wrong", "1.0", "end")
        for i, char in enumerate(target):
            start_index = f"1.0+{i}c"
            end_index = f"1.0+{i+1}c"
            if i < len(user_text):
                if user_text[i] == target[i]:
                    self.target_display.tag_add("right", start_index, end_index)
                else:
                    self.target_display.tag_add("wrong", start_index, end_index)
        self.target_display.config(state="disabled")

    def progress_to_next_line(self):
        current_text = self.text_area.get("1.0", "end-1c")
        target = self.lesson_lines[self.current_line_index]
        correct_chars = sum(1 for i, ch in enumerate(current_text)
                            if i < len(target) and ch == target[i])
        self.total_chars_typed += len(current_text)
        self.cumulative_correct_chars += correct_chars
        self.error_count += len(current_text) - correct_chars
    
        if self.current_line_index < len(self.lesson_lines) - 1:
            self.current_line_index += 1
            next_line = self.lesson_lines[self.current_line_index]
            self.target_display.config(state="normal")
            self.target_display.delete("1.0", "end")
            self.target_display.insert("1.0", next_line)
            self.target_display.config(state="disabled")
            self.text_area.delete("1.0", "end")
            self.update_next_finger()
        else:
            self.test_finished = True
            self.analysis_shown = True
            self.text_area.config(state="disabled")
            self.root.after(200, self.show_analysis)
    
    def update_next_finger(self):
        self.left_hand.clear_highlights()
        self.right_hand.clear_highlights()
        for key, btn_list in self.key_buttons.items():
            for btn in btn_list:
                btn.config(background=btn.original_bg)
        
        if self.lesson_lines:
            target = self.lesson_lines[self.current_line_index]
        else:
            target = self.target_text
        
        next_index = len(self.text_area.get("1.0", "end-1c"))
        if next_index < len(target):
            next_char = target[next_index]
            shift_mapping = {
                "~": "`", "!": "1", "@": "2", "#": "3", "$": "4", "%": "5",
                "^": "6", "&": "7", "*": "8", "(": "9", ")": "0",
                "_": "-", "+": "=", "{": "[", "}": "]", "|": "\\",
                ":": ";", "\"": "'", "<": ",", ">": ".", "?": "/"
            }
            shift_required = False
            if next_char.isalpha() and next_char.isupper():
                shift_required = True
            elif next_char in shift_mapping:
                shift_required = True
            
            if shift_required:
                if next_char.isalpha():
                    finger_key = next_char.upper()
                    virtual_key = next_char.upper()
                else:
                    finger_key = next_char  
                    virtual_key = shift_mapping.get(next_char, next_char)
            else:
                if next_char == " ":
                    finger_key = "Space"
                    virtual_key = "Space"
                elif next_char.isalpha():
                    finger_key = next_char.upper()
                    virtual_key = next_char.upper()
                else:
                    finger_key = next_char
                    virtual_key = next_char
            
            if shift_required and finger_key in self.finger_mapping:
                letter_hand, finger_region = self.finger_mapping[finger_key]
                if letter_hand == "left":
                    self.left_hand.highlight_finger(finger_region)
                elif letter_hand == "right":
                    self.right_hand.highlight_finger(finger_region)
                shift_hand = "right" if letter_hand == "left" else "left"
                if shift_hand == "left":
                    self.left_hand.highlight_finger("pinky_top")
                elif shift_hand == "right":
                    self.right_hand.highlight_finger("pinky_top")
                if virtual_key in self.key_buttons:
                    for btn in self.key_buttons[virtual_key]:
                        btn.config(background="green")
                if "Shift" in self.key_buttons:
                    for btn in self.key_buttons["Shift"]:
                        if hasattr(btn, "shift_side") and btn.shift_side == shift_hand:
                            btn.config(background="green")
            else:
                if finger_key in self.finger_mapping:
                    hand_side, finger_region = self.finger_mapping[finger_key]
                    if hand_side == "right" and finger_key == "Space":
                        self.right_hand.highlight_finger(finger_region)
                    if hand_side == "left":
                        self.left_hand.highlight_finger(finger_region)
                    elif hand_side == "right":
                        self.right_hand.highlight_finger(finger_region)
                if virtual_key in self.key_buttons:
                    for btn in self.key_buttons[virtual_key]:
                        btn.config(background="green")

    def show_analysis(self):
        total_time = self.final_elapsed_time
        avg_speed = self.final_speed
        overall_accuracy = self.final_accuracy
        error_count = self.final_errors
    
        times = [t for t, w, a in self.history]
        wpms = [w for t, w, a in self.history]
        accuracies = [a for t, w, a in self.history]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        fig.suptitle("Typing Analysis", fontsize=16)
        ax1.plot(times, wpms, marker='o', color='blue')
        ax1.set_title("Speed (WPM) Over Time")
        ax1.set_xlabel("Time (seconds)")
        ax1.set_ylabel("Words Per Minute")
        ax1.grid(True)
        ax2.plot(times, accuracies, marker='o', color='green')
        ax2.set_title("Accuracy Over Time")
        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Accuracy (%)")
        ax2.set_ylim(0, 110)
        ax2.grid(True)
        
        summary_text = (f"Total Time: {total_time:.1f} sec   "
                        f"Avg Speed: {avg_speed:.1f} WPM   "
                        f"Avg Accuracy: {overall_accuracy:.1f}%   "
                        f"Errors: {error_count}")
        fig.text(0.5, 0.01, summary_text, ha='center', fontsize=12)
        
        plt.tight_layout(rect=[0, 0.08, 1, 0.95])
        plt.show()
    
###################################
# 3) Run the App
###################################
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
