import sys
import os
import numpy as np
from scipy.optimize import linear_sum_assignment

historia_obiektow = {}
prog_dystansu = 50
min_podobienstwo = 0.3

def srodek_bbox(bbox):
    x, y, w, h = bbox
    return x + w/2, y + h/2

def dystans_bbox(bbox1, bbox2):
    c1 = srodek_bbox(bbox1)
    c2 = srodek_bbox(bbox2)
    return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def podobienstwo_obszaru(bbox1, bbox2):
    area1 = bbox1[2] * bbox1[3]
    area2 = bbox2[2] * bbox2[3]
    if max(area1, area2) == 0:
        return 0
    return min(area1, area2) / max(area1, area2)

def numer_ramki(nazwa):
    return int(nazwa.split('_')[-1].split('.')[0])

def predykcja_pozycji(historia, delta_ramek):
    if len(historia) < 2:
        return None
    pos1, pos2 = historia[-2], historia[-1]
    vx = pos2[0] - pos1[0]
    vy = pos2[1] - pos1[1]
    return [pos2[0] + vx * delta_ramek, pos2[1] + vy * delta_ramek, pos2[2], pos2[3]]

def macierz_kosztow(obecne, poprzednie, delta):
    if not poprzednie or not obecne:
        return np.zeros((len(obecne), len(poprzednie)))
    
    koszty = np.full((len(obecne), len(poprzednie)), 999.0)
    
    for i, bbox_o in enumerate(obecne):
        for j, bbox_p in enumerate(poprzednie):
            dist = dystans_bbox(bbox_o, bbox_p) / delta
            sim = podobienstwo_obszaru(bbox_o, bbox_p)
            
            if dist < prog_dystansu and sim > min_podobienstwo:
                koszt_dist = dist / prog_dystansu
                koszt_sim = 1.0 - sim
                
                bonus = 0.0
                if j in historia_obiektow and len(historia_obiektow[j]) >= 2:
                    pred = predykcja_pozycji(historia_obiektow[j], delta)
                    if pred:
                        pred_dist = dystans_bbox(bbox_o, pred)
                        if pred_dist < prog_dystansu:
                            bonus = 0.25 * (1.0 - pred_dist / prog_dystansu)
                
                koszty[i, j] = max(0.0, 0.6 * koszt_dist + 0.4 * koszt_sim - bonus)
    
    return koszty

def przypisz_obiekty(obecne, poprzednie, delta=1):
    if not poprzednie:
        return [-1] * len(obecne)
    
    koszty = macierz_kosztow(obecne, poprzednie, delta)
    if koszty.size == 0:
        return [-1] * len(obecne)
    
    rows, cols = linear_sum_assignment(koszty)
    przypisania = [-1] * len(obecne)
    
    for r, c in zip(rows, cols):
        if koszty[r, c] < 0.75:
            przypisania[r] = c
    
    return przypisania

def wczytaj_dane(plik, z_id=False):
    dane = {}
    try:
        with open(plik, 'r') as f:
            linie = f.readlines()
    except:
        return dane
    
    i = 0
    while i < len(linie):
        linia = linie[i].strip()
        if linia.endswith('.jpg'):
            nazwa = linia
            dane[nazwa] = []
            i += 1
            if i >= len(linie):
                break
            
            count = int(linie[i].strip())
            i += 1
            
            for _ in range(count):
                if i < len(linie):
                    vals = list(map(float, linie[i].strip().split()))
                    if z_id:
                        dane[nazwa].append((int(vals[0]), vals[1:]))
                    else:
                        dane[nazwa].append(vals)
                    i += 1
        else:
            i += 1
    
    return dane

def aktualizuj_historie(track_id, bbox):
    center = srodek_bbox(bbox)
    pos = [center[0], center[1], bbox[2], bbox[3]]
    
    if track_id not in historia_obiektow:
        historia_obiektow[track_id] = []
    
    historia_obiektow[track_id].append(pos)
    if len(historia_obiektow[track_id]) > 4:
        historia_obiektow[track_id].pop(0)

def sledz_obiekty(folder, tylko_eval=False, plik_wyj=None):
    historia_obiektow.clear()
    
    plik_bbox = os.path.join(folder, "bboxes.txt")
    ramki = wczytaj_dane(plik_bbox)
    
    kolejnosc = sorted(ramki.keys(), key=numer_ramki)
    
    wyj = open(plik_wyj, 'w') if plik_wyj else None
    wyniki = {}
    poprz_nazwa = None
    poprz_bbox = None
    
    for nazwa in kolejnosc:
        obecne_bbox = ramki[nazwa]
        
        if poprz_bbox is None:
            przypisania = [-1] * len(obecne_bbox)
        else:
            delta = numer_ramki(nazwa) - numer_ramki(poprz_nazwa)
            przypisania = przypisz_obiekty(obecne_bbox, poprz_bbox, delta)
            
            for i, track_id in enumerate(przypisania):
                if track_id >= 0:
                    aktualizuj_historie(track_id, obecne_bbox[i])
        
        wyniki[nazwa] = list(zip(przypisania, obecne_bbox))
        
        if not tylko_eval:
            tekst = f"{nazwa}\n{len(obecne_bbox)}\n"
            for przyp, bbox in wyniki[nazwa]:
                tekst += f"{przyp} {' '.join(map(str, bbox))}\n"
            
            print(tekst.strip())
            if wyj:
                wyj.write(tekst)
        
        poprz_bbox = obecne_bbox
        poprz_nazwa = nazwa
    
    if wyj:
        wyj.close()
    
    return wyniki

def ocen_dokladnosc(wyniki, gt):
    total = 0
    correct = 0
    
    wspolne = set(wyniki.keys()) & set(gt.keys())
    for ramka in wspolne:
        gt_ids = [x[0] for x in gt[ramka]]
        pred_ids = [x[0] for x in wyniki[ramka]]
        
        for i, pid in enumerate(pred_ids):
            if i < len(gt_ids) and pid == gt_ids[i]:
                correct += 1
            total += 1
    
    return (correct / total * 100) if total > 0 else 0

def main(folder):
    wyj_plik = os.path.join(folder, "wynik.txt")
    gt_plik = os.path.join(folder, "bboxes_gt.txt")
    
    if not os.path.exists(gt_plik):
        sledz_obiekty(folder, plik_wyj=wyj_plik)
    else:
        gt = wczytaj_dane(gt_plik, z_id=True)
        wyniki = sledz_obiekty(folder, tylko_eval=True)
        dokladnosc = ocen_dokladnosc(wyniki, gt)
        sledz_obiekty(folder, plik_wyj=wyj_plik)
        print(f"\nSkuteczność: {dokladnosc:.2f}%")
        print(f"Zapisano: {wyj_plik}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        main('')
    else:
        main(sys.argv[1])
