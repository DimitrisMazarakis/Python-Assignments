import math
import random
import copy
import argparse

def add_circle(new_metopo,px,py,pr,current_closest_circle,file_name,tuxaies,akt,empty,items,output_name):#o (px,py,pr) kuklos pou prostethike teleutaios
    sunte_sximatos={}
    if empty==False:
        sunte_sximatos=open_file(file_name)
    telos=False
    kukloi=2
    while len(total_circles)<items and telos==False:#posoi komvoi tha prostethoun
        alive=[]
        for circle in new_metopo:
            alive.append(circle)#gemizw tous zwntanous
        new_circle,new_metopo,current_closest_circle,cn,telos=find_circle_to_add(new_metopo,alive,sunte_sximatos,tuxaies,akt,empty)#tha mporouse na epistrefei kai to closest_circle
        kukloi+=1
        if telos==True:
            kukloi-=1
            break
        (kx,ky,kr)=new_circle
        new_metopo[(current_closest_circle)]=[new_circle]#o prwtos kuklos exei epomeno ton teleutaio
        new_metopo[new_circle]=[cn]#px vazw ton 40 na deixnei ton 28 kai oxi ton 39
        total_circles.append((kx,ky,kr))#vazw ton neo kuklo stin lista
    print(kukloi)#posoi kukloi mphkan
    with open(str(output_name), 'a') as f:#to grafei sto arxeio
        for circle in total_circles:
            a,b,c=circle
            f.write(str(a)+" "+str(b)+" "+str(c)+"\n")
        if empty==False:
            with open(file_name, 'r') as file:
                shape = file.read()
            f.write(str(shape))

def find_circle_to_add(new_metopo,alive,sunte_sximatos,tuxaies,akt,empty):#vriskei pou tha mpei o neos kuklos
    deleted=0
    telos=False
    vriskei_tixo=True
    cms=[]
    copy_metopo={}
    recover=[]
    aktines=[]#apothikeuei tis aktines an den xrisimopoiithoun gia ton epomeno
    while vriskei_tixo==True:#tha teleiwsei mono otan ginei False
        cm=find_closest_to_center(new_metopo,alive)
        (mx,my,rm)=cm
        cms.append(cm)
        mpike=False  #an temnei kapoion kuklo to c
        for circle in new_metopo:
            if new_metopo[cm][0]==circle:
                (nx,ny,rn)=circle#xwrizoyme ta stoixeia tou kuklo Cn
                cn=(nx,ny,rn)#teleutaios koiklos tou metopou
        prospathia=1
        while mpike==False:
            if tuxaies==True:#tuxaies aktines
                if len(aktines)==0:
                    r=random.randint(5,10)
                    aktines.append(r)
                else:
                    r=aktines.pop()
                    aktines.append(r)
            else:#sugkekrimeni aktina
                r=akt
            dx=nx-mx
            dy=ny-my
            d=math.sqrt(dx**2+dy**2)
            r1=r+rm
            r2=r+rn
            l=(r1**2-r2**2+d**2)/(2*d**2)
            e=math.sqrt((r1**2/d**2)-l**2)
            (kx,ky,kr)=(round(mx+l*dx-e*dy,2),round(my+l*dy+e*dx,2),r)#dimiourgw nea aktina
            new_circle=(kx,ky,kr) #Ci
            mpike=True
            for circle in new_metopo:
                (a,b,ar)=circle
                distance=round(math.sqrt((a-kx)**2+(b-ky)**2),2)
                if ar+kr>distance and circle!=cm and circle!=cn:#temnei ton circle
                    mpike=False
            if mpike==False: #dld temnei kapoion kuklo
                count_circles=0
                cj_count=0#gia na vrw ton Cj
                cm_found=False
                circle=new_metopo[cn][0]#ksekiname apo ton cn mexri na vroume ton cm
                (tx,ty,tr)=circle#gia na mhn allazw ta nx,ny,nr kathe fora
                cj2=(0,0,0)
                while cm_found==False:
                    distance=round(math.sqrt((tx-kx)**2+(ty-ky)**2),2)
                    if tr+kr>distance and circle!=cm:#temnei ton circle
                        if cj_count==0:#vrikame to prwto Cj
                            cj=circle
                            cj_count+=1
                            bnj=count_circles
                        else:#temnei kai deutero
                            cj2=circle
                            cj_count+=1
                    if circle==cm:#an o epomenos tou circle einai o cm stamatame
                        cm_found=True #ftasame ston cm
                    else:
                        circle=new_metopo[circle][0]
                        (tx,ty,tr)=circle
                        count_circles+=1 #gia na vroume ta bmj kai bmj2
                if cj_count>0:
                    if cj_count==1:#temnei mono enan o ci
                        cj2=cj
                        bmj2=0
                        circle=cj2
                        while circle!=cm:#vriskw plithos kuklwn metaksi cm kai cj2=cj
                            circle=new_metopo[circle][0]
                            if circle!=cm:
                                bmj2+=1
                    else: #temnetai kai me allous ektos ton cj
                        bmj2=0
                        circle=cj2
                        while circle!=cm:#vriskw plithos kuklwn metaksi cm kai cj2
                            circle=new_metopo[circle][0]
                            if circle!=cm:
                                bmj2+=1
                    if empty==False and prospathia==1:
                        copy_metopo=copy.deepcopy(new_metopo)#gia na epanaferw tous diegramenous
                        prospathia+=1
                    if bmj2<bnj:# tote pairnoume cj2 pou proeigeitai tou cm
                        cj=cj2
                        new_metopo,alive,recover,deleted=delete_circle(new_metopo,cj,cn,alive,recover)# diagrafei tous kuklous
                        cm=cj#thetw cm iso me cj
                        (mx,my,rm)=cj
                    else: #pairnei kai to iso??
                        new_metopo,alive,recover,deleted=delete_circle(new_metopo,cm,cj,alive,recover)# diagrafei tous kuklous
                        cn=cj#thetw cn iso me cj
                        (nx,ny,rn)=cj
        if empty==False:
            fits=find_if_it_fits(sunte_sximatos,new_circle)
            if fits:#xwraei o neos kuklos
                vriskei_tixo=False
            else:
                if deleted>0:
                    new_metopo=copy.deepcopy(copy_metopo)#epanaferw autous pou diegrapsa
                for dead in recover:#epanaferw tous nekrous
                    if (dead not in cms):
                        alive.append(dead)#gemizw tous zwntanous
                recover=[]
                if cm in alive:
                    alive.remove(cm)
            if len(alive)==0:#den xwrane alloi
                vriskei_tixo=False#stop
                telos=True
        else:
            vriskei_tixo=False#na min elegxei an vriskei tixo
    return new_circle,new_metopo,cm,cn,telos#den temnei kapoion kuklo 

def find_if_it_fits(sunte_sximatos,new_circle):
    fits=True
    (cx,cy,cr)=new_circle
    for node in sunte_sximatos:
        for spot in sunte_sximatos[node]:
            (ux,uy)=node
            (vx,vy)=spot
            l2=(ux-vx)**2+(uy-vy)**2
            if l2==0: #sumpiptoun ta simeia
                distance=round(math.sqrt((ux-cx)**2+(uy-cy)**2),2)
            else:
                t=((cx-ux)*(vx-ux)+(cy-uy)*(vy-uy))/l2
                t=max(0,min(1,t))
                ppx=ux+t*(vx-ux)
                ppy=uy+t*(vy-uy)
                distance=round(math.sqrt((ppx-cx)**2+(ppy-cy)**2),2)
            if distance<cr:
                fits=False
    return fits

def open_file(space_file):#anoigei to arxeio tou xwrou
    g = {}
    with open(space_file) as rectangle:
        for line in rectangle:
            nodes = [float(x) for x in line.split()]
            if len(nodes) != 4:
                continue
            node1=(nodes[0],nodes[1])
            node2=(nodes[2],nodes[3])
            if node1 not in g:
                g[node1] = []
            if node2 not in g:
                g[node2] = []
            g[node1].append(node2)
            g[node2].append(node1) 
    return g

def find_closest_to_center(new_metopo,alive):#vriskei ton kiklo tou metopou pou einai pio konta sto simeio ekkinisis
    min_dist=10000000
    min_circle=(0,0,0)#tha allaksei sigoura
    for circle in new_metopo:
        (cx,cy,cr)=circle
        distance=round(math.sqrt(cx**2+cy**2),2)#xwris na mas noiazei h aktina
        if (distance<min_dist) and (circle in alive): #kai einai zwntanos o kuklos
            min_circle=circle
            min_dist=distance
    return min_circle

def delete_circle(new_metopo,first,last,alive,recover):
    deleted_circles=[]
    circle=new_metopo[first][0]#o epomenos tou prwtou
    while circle!=last:
        deleted_circles.append(circle)
        circle=new_metopo[circle][0]
    for circle in deleted_circles:
        del new_metopo[circle]#diagrafei ton kuklo apo to metopo
        if circle in alive:
            recover.append(circle)#gia na tous ksana zwntanepsw
            alive.remove(circle)#diagrafw ap tous zwntanous
    new_metopo[first][0]=last
    return new_metopo,alive,recover,len(deleted_circles)

parser = argparse.ArgumentParser(description='Count circles')
parser.add_argument('-i','--items','-items')
parser.add_argument('-r','--radius')
parser.add_argument('--min_radius')
parser.add_argument('--max_radius')
parser.add_argument('-s','--seed')
parser.add_argument('-b','--b')
parser.add_argument('output_file')
args=parser.parse_args()
if (args.seed):
    random.seed(int(args.seed))
    tuxaies=True
    fr=random.randint(int(args.min_radius),int(args.max_radius))
    sr=random.randint(int(args.min_radius),int(args.max_radius))
else:
    tuxaies=False
    fr=int(args.radius)
    sr=int(args.radius)
metopo = {
  (0.00,0.00,fr): [(fr+sr,0.00,sr)],
  (fr+sr,0.00,sr): [(0.00,0.00,fr)]
}
total_circles=[]
total_circles.append((0.00,0.00,fr))
total_circles.append((fr+sr,0.00,sr))
(sx,sy,r)=(0.00,0.00,fr)#simeio ekkinisis 
start_point=(sx,sy,r)
empty=True
folder=None
if(args.b):
    folder=args.b
    empty=False
if args.items:
    items=int(args.items)
else:
    items=100000000
add_circle(metopo,fr+sr,0,sr,start_point,folder,tuxaies,fr,empty,items,args.output_file)