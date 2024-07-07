import tkinter as tk;
from random import randint;
import math;
from sklearn.cluster import KMeans

win = tk.Tk();
win.title("KMeans");
win.geometry("1150x700");

RED    = "#f00000";
GREEN  = "#00ff00";
BLUE   = "#0000ff";
YELLOW = "#f9cf53";
PURPLE = "#fb007d";
SKY    = "#00ffff";
ORANGE = "#ff7d19";
GRAPE  = "#64197d";
GRASS  = "#379b41";

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

points, clusters, labels = [], [], [];
K, Error = 0, 0;

def motion(event):
    position_label.config(text=f"{event.x, event.y}");
def get_points(event):
    points.append([event.x, event.y]);
def draw_circle(x, y, r, color):
    radius = r;
    x0 = x - radius; y0 = y - radius;
    x1 = x + radius; y1 = y + radius;
    panel.create_oval(x0, y0, x1, y1, outline="black", fill=color, width=2);
def draw_points(event):
    draw_circle(event.x, event.y, 5, "#fafafa");
def K_increase(event):
    global K;
    if K < 9: K += 1;
    k_text.config(text=f"K = {K}");
def K_decrease(event):
    global K;
    if K > 0: K -= 1;
    k_text.config(text=f"K = {K}");
def update_panel():
    panel.delete('all');
    if list(labels) == []:
        for point in points:
            draw_circle(point[0], point[1], 5, "#fafafa");
    else:
        for i in range(len(points)):
            draw_circle(points[i][0], points[i][1], 5, COLORS[labels[i]]);
def draw_clusters(clusters):
    for i in range(len(clusters)):
        draw_circle(clusters[i][0], clusters[i][1], 7, COLORS[i]);
def random_cluster(event):
    global clusters, points;
    clusters= [];
    update_panel();
    for i in range(K):
        clusters.append([randint(0, 690), randint(0, 540)]);
    draw_clusters(clusters);
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]));
def assign_label(clusters, points):
    labels = [];
    for point in points:
        distances_to_cluster = [];
        for cluster in clusters:
            distances_to_cluster.append(distance(point, cluster));
        min_distance = min(distances_to_cluster);
        labels.append(distances_to_cluster.index(min_distance));
    return labels;
def update_clusters(labels, points, clusters):
    for i in range(len(clusters)):
        count, sum_x, sum_y = 0, 0, 0;
        for j in range(len(points)):
            if labels[j] == i:
                sum_x += points[j][0];
                sum_y += points[j][1];
                count += 1;
        if not count == 0:
            clusters[i] = [int(sum_x/count), int(sum_y/count)];
        else:
            clusters[i] = [randint(0, 690), randint(0, 540)];
    return clusters;
def error_handle(points, clusters):
    Error = 0;
    for point in points:
        for cluster in clusters:
            Error += distance(point, cluster);
    error_label.config(text =f"ERROR: {int(Error)}");
def run_func(event):
    global Error, labels, clusters, points;
    if list(points) == [] or list(clusters) == []: return;
    Error = 0;
    labels = assign_label(clusters, points);
    clusters = update_clusters(labels, points, clusters);
    update_panel();
    draw_clusters(clusters);
    error_handle(clusters, points);
def algorithm_func(event):
    global labels, points, clusters;
    try:
        Error = 0;
        kmeans = KMeans(n_clusters=K).fit(points);
        labels = kmeans.predict(points);
        clusters = kmeans.cluster_centers_;
        for point in points:
            for cluster in clusters:
                Error += int(distance(point, cluster));
        update_panel();
        draw_clusters(clusters);
        error_label.config(text =f"ERROR: {int(Error)}");
    except: print("error");
def reset_func(event):
    global K, Error, points, clusters, labels;
    K, Error = 0, 0;
    points, clusters, labels = [], [], [];
    panel.delete('all');
    error_label.config(text="ERROR: 0");
    k_text.config(text="K = 0");

# Draw Panel
background_panel = tk.Canvas(win, width=700, height=550, bg="black");
background_panel.place(x = 50, y = 50);
panel = tk.Canvas(win, width= 690, height=540, bg="white");
panel.place(x = 55, y = 55);
# Draw K +
plus_btn = tk.Button(win, text="+", width=3, height=2, bg="black", fg="white", font=('Arial', 16));
plus_btn.place(x = 800, y = 50);
# Draw text K;
k_text = tk.Label(win, text=f"K = {K}", font = ("Arial", 30));
k_text.place(x = 900, y = 50);
# Draw K -
minus_btn = tk.Button(win, text="-", width=3, height=2, bg="black", fg="white", font=('Arial', 16));
minus_btn.place(x = 1050, y = 50);
# Draw run btn
run_btn = tk.Button(win, text="RUN", width=18, height=1, bg = "black", fg = "white", font = ('Arial', 20));
run_btn.place(x = 800, y = 150);
# Draw Random btn
random_btn = tk.Button(win, text="RANDOM", width=18, height=1, bg = "black", fg = "white", font = ('Arial', 20));
random_btn.place(x = 800, y = 250);
# Draw Error label
error_label = tk.Label(win, text=f"ERROR: {Error}", font = ("Arial", 20));
error_label.place(x = 840, y = 350);
# Draw Algorithm btn
algorithm_btn = tk.Button(win, text="ALGORITHM", width=18, height=1, bg = "black", fg = "white", font = ('Arial', 20));
algorithm_btn.place(x = 800, y = 430);
# Draw Reset btn
reset_btn = tk.Button(win, text="RESET", width=18, height=1, bg = "black", fg = "white", font = ('Arial', 20));
reset_btn.place(x = 800, y = 530);
# Draw pointer position
position_label = tk.Label(win, text="(0, 0)", font=('Arial', 12));
position_label.place(x = 55, y = 20);

# Event handle
panel.bind("<Button-1>", get_points);
panel.bind("<Button-1>", draw_points, add="+");
panel.bind("<Motion>", motion);
plus_btn.bind("<Button-1>", K_increase);
minus_btn.bind("<Button-1>", K_decrease);
random_btn.bind("<Button-1>", random_cluster);
run_btn.bind("<Button-1>", run_func);
algorithm_btn.bind("<Button-1>", algorithm_func);
reset_btn.bind("<Button-1>", reset_func);
win.mainloop();