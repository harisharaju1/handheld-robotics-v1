import math, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'cad'))
import params as P
OUT = pathlib.Path(__file__).resolve().parent
R=P.DECK_D/2
standoffs=list(P.STANDOFF_PTS)
FOOT_CY=P.FOOT_CY
FX,FY=P.BRACKET_FOOT[0]/2,P.BRACKET_FOOT[1]/2
gx,gy=FX+P.FOOT_MARK_GAP,FY+P.FOOT_MARK_GAP
footmarks=[(a*gx,s*(FOOT_CY+b*gy)) for s in (1,-1) for a in (-1,1) for b in (-1,1)]
casters=[(cx,sy*P.CASTER_PITCH/2) for cx in (P.CASTER_X,-P.CASTER_X) for sy in (-1,1)]
bx,by=P.BATT_TRAY_CENTER
tray=[(bx+x,by+y) for x,y in P.TRAY_HOLES]
ex,ey=P.EPLATE_CENTER; esx,esy=P.EPLATE_SIZE
eplate=[(ex+a*(esx/2-6),ey+b*(esy/2-6)) for a in (-1,1) for b in (-1,1)]
mx,my=P.MAST_CENTER
mast=[(mx+19*a,my+19*b) for a,b in ((1,0),(-1,0),(0,1),(0,-1))]
cx_,cy_=P.MODULE_CENTER
module=[(cx_+sx*P.MODULE_DECK_SQ,cy_+sy*P.MODULE_DECK_SQ) for sx in (-1,1) for sy in (-1,1)]
px,py=P.PI_CENTER
pi=[(px+a*29,py+b*24.5) for a in (-1,1) for b in (-1,1)]
WSX,WSY0=P.WHEEL_SLOT_HALF_X,P.WHEEL_SLOT_Y0
lower={'name':'LOWER DECK','holes':[('standoff',standoffs),('caster',casters),('battery tray',tray),('electronics plate',eplate)],'marks':footmarks,'wheels':True}
upper={'name':'UPPER DECK','holes':[('standoff',standoffs),('mast',mast),('module plate',module),('Raspberry Pi',pi)],'marks':[],'wheels':False}
DRILL=4.0
def outline(ax,deck):
    if deck['wheels']:
        # circle arcs between wheel slots + slot edges
        a0=math.degrees(math.asin(WSX/R))
        segs=[]
        for c in (90,-90):
            pass
        th=np.linspace(0,2*np.pi,2000); xs=R*np.cos(th); ys=R*np.sin(th)
        keep=~((np.abs(xs)<WSX)&(np.abs(ys)>WSY0))
        # draw arcs piecewise
        idx=np.where(keep)[0]; br=np.where(np.diff(idx)>1)[0]
        for part in np.split(idx,br+1):
            ax.plot(xs[part],ys[part],'k',lw=1.2)
        yr=math.sqrt(R*R-WSX*WSX)
        for s in (1,-1):
            ax.plot([-WSX,-WSX,WSX,WSX],[s*yr,s*WSY0,s*WSY0,s*yr],'k',lw=1.2)
            ax.add_patch(Polygon([(-WSX,s*WSY0),(WSX,s*WSY0),(WSX,s*yr),(-WSX,s*yr)],closed=True,fill=False,hatch='///',lw=0,color='0.5'))
            ax.text(0,s*(WSY0+12),'CUT OUT\n(wheel slot)',ha='center',va='center',fontsize=7,color='0.25')
    else:
        ax.add_patch(Circle((0,0),R,fill=False,lw=1.2,color='k'))
    # cable slot 40 x 14 (stadium)
    ax.add_patch(FancyBboxPatch((-13,-7),26,14,boxstyle='round,pad=0,rounding_size=7',fill=False,lw=1,hatch='///',color='k'))
    ax.text(0,-12,'CUT OUT 40 x 14 slot\n(drill 2 x 14 mm at ends, jigsaw between)',ha='center',va='top',fontsize=5.5)
def holes(ax,deck):
    n=0
    for label,pts in deck['holes']:
        for (x,y) in pts:
            ax.add_patch(Circle((x,y),DRILL/2,fill=False,lw=0.6,color='k'))
            ax.plot([x-4,x+4],[y,y],'k',lw=0.35); ax.plot([x,x],[y-4,y+4],'k',lw=0.35)
            n+=1
    for (x,y) in deck['marks']:
        ax.add_patch(Circle((x,y),1.0,fill=True,color='k')); n+=1
    if deck['marks']:
        for s_ in (1,-1):
            ax.add_patch(Rectangle((-FX,s_*FOOT_CY-FY),2*FX,2*FY,fill=False,ls='--',lw=0.7,color='k'))
            ax.text(0,s_*FOOT_CY,'MOTOR BRACKET FOOT\n(bolts to the UNDERSIDE)\n2 mm dots = locating marks\nat its corners. Drill its 4\nholes through the bracket.',
                    ha='center',va='center',fontsize=5.5)
    return n
def common(ax,deck,show_text=True):
    outline(ax,deck); n=holes(ax,deck)
    ax.plot([-6,6],[0,0],'k',lw=0.4); ax.plot([0,0],[-6,6],'k',lw=0.4)
    # axis / orientation
    ax.annotate('',xy=(95,-8),xytext=(55,-8),arrowprops=dict(arrowstyle='->',lw=0.9))
    ax.text(75,-5,'FRONT (+X)',ha='center',fontsize=7,weight='bold')
    ax.text(-62,98,'LEFT side (+Y)',ha='center',fontsize=6)
    return n
def header(ax,deck,n,x0,y0,extra=''):
    ax.text(x0,y0,f"{deck['name']} - 1:1 TEMPLATE  (handheld-robotics-v1, Nov 2026, direct-mount)",fontsize=9,weight='bold',va='top')
    ax.text(x0,y0-6,f"Print at 100% / 'Actual size' - NOT 'fit to page'. Check the 100 mm bar first.\n"
            f"{n} holes: centre-punch each crosshair, drill 3 mm pilot, then open to {DRILL:.0f} mm (black dots: 2 mm). Scrap wood behind.\n"
            f"Outer line = cut line (250 mm circle). Hatched = remove. Top face up; deck is symmetric left-right.{extra}",fontsize=6,va='top')
def scalebar(ax,x,y):
    ax.add_patch(Rectangle((x,y),100,4,fill=False,lw=0.8,color='k'))
    for i in range(11): ax.plot([x+10*i]*2,[y,y+(4 if i%5==0 else 2)],'k',lw=0.5)
    ax.text(x+50,y+6,'100 mm - measure this',ha='center',fontsize=6)
def page(pdf,W,H,xl,yl,draw):
    fig=plt.figure(figsize=(W/25.4,H/25.4)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')
    draw(ax); pdf.savefig(fig); plt.close(fig)
# A3 portrait 297 x 420: one deck per page
with PdfPages(OUT/'deck_templates_A3.pdf') as pdf:
    for d in (lower,upper):
        def dr(ax,d=d):
            n=common(ax,d); header(ax,d,n,-138,200); scalebar(ax,-50,-185)
        page(pdf,297,420,(-148.5,148.5),(-210,210),dr)
# A4 landscape 297 x 210: two halves per deck, 20 mm overlap, align on the dashed centre line
with PdfPages(OUT/'deck_templates_A4_tiled.pdf') as pdf:
    for d in (lower,upper):
        for half,(ylo,yhi) in (('LEFT half (+Y)',(-15,195)),('RIGHT half (-Y)',(-195,15))):
            def dr(ax,d=d,half=half,ylo=ylo,yhi=yhi):
                n=common(ax,d)
                ax.plot([-140,140],[0,0],'k--',lw=0.5)
                for x in (-120,-60,60,120):
                    ax.plot([x-5,x+5],[10,10],'k',lw=0.5); ax.plot([x,x],[5,15],'k',lw=0.5)
                    ax.plot([x-5,x+5],[-10,-10],'k',lw=0.5); ax.plot([x,x],[-5,-15],'k',lw=0.5)
                ax.text(-140, 1, 'tape here: overlap the two sheets so both dashed lines + crosshairs coincide', fontsize=5)
                if ylo<0 and yhi>100:
                    header(ax,d,n,-145,yhi-4,extra=f"\nSheet: {half}.")
                    scalebar(ax,40,-12) if False else scalebar(ax,-145,yhi-40)
                else:
                    header(ax,d,n,-145,ylo+44,extra=f"\nSheet: {half}.")
                    scalebar(ax,-145,ylo+6)
            page(pdf,297,210,(-148.5,148.5),(ylo,yhi),dr)
print('done')
