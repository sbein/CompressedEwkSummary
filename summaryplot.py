import ROOT
ROOT.gROOT.SetBatch(1)
import os
from array import array
ROOT.gStyle.SetOptStat(0)

tl = ROOT.TLatex()
tl.SetNDC()

doHLLHC = False
drawRadiativeBound = True


def main():
    analyses = {}
    analyses['#splitline{Disappearing Track}{arXiv:2309.16823}'] = ['results_sus_21_006/PureHiggsino_DTRun2_results.root', 'Exp_PureHiggsino_DTRun2', 'Obs_PureHiggsino_DTRun2', ROOT.kSpring+2]#ROOT.kViolet-1 
    analyses['#splitline{Isolated Soft Track}{SUS-24-012}'] = ['results_sus_24_012/PureHiggsino_SDPRun2_results.root', 'Exp_PureHiggsino_SDPRun2', 'Obs_PureHiggsino_SDPRun2', ROOT.kOrange-1]#ROOT.kGreen-1 
    #analyses['#splitline{Recursive Jigsaw}{SUS-23-004}'] = ['results_sus_23_004/B135_bugfix16_HinoN2C1Super_xsec_smooth_canv.root', 'gr_mid', 'gr_obs', ROOT.kGray]
    analyses['#splitline{Soft lepton+track}{SUS-24-003}'] = ['results_sus_24_003/PureHiggsino_spdl_Run2comb_results.root', 'Exp_PureHiggsino_spdl_comb', 'Obs_PureHiggsino_spdl_comb', ROOT.kViolet]
    #analyses['SUS-24-003'] = ['results_sus_24_003/PureHiggsino_spdl_Run2comb_results.root', 'Exp_PureHiggsino_spdl_comb', 'Obs_PureHiggsino_spdl_comb', ROOT.kRed]
    analyses['#splitline{Soft 2l and 3l}{EXO-23-017}'] = ['results_exo_23_017/h2lim_20250226_Hino_neg_allEEMM_neg_0.0_log_smooth1k5a_dMc1n1.root', 'limitGraph_0', 'limitGraph_obs', ROOT.kAzure-9]
    
    if 'Recursive Jigsaw' in ','.join(list(analyses.keys())): xmax, ymax = 300, 100
    else: xmax, ymax = 250, 5
    
    analysis_names = list(analyses.keys())
    analysis_names.reverse()
    if doHLLHC:
        for analysis_name in analysis_names:
            analysis = analyses[analysis_name]
            analysis[0] = analysis[0].replace('Run2','HLLHC')
            analysis[2] = ''
                
    canvas = ROOT.TCanvas("c1", "SUSY EW Summary Plot", 800, 600)
    print(canvas.GetTopMargin(), canvas.GetBottomMargin())
    canvas.SetBottomMargin(0.15)
    canvas.SetTopMargin(1.3)
    
    mg = ROOT.TMultiGraph()
    legend0 = ROOT.TLegend(0.12, 0.88, 0.80, 0.98)
    legend0.SetHeader("#bf{pp#rightarrow#tilde{#chi}^{0}_{2}#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{0}_{2}#tilde{#chi}^{0}_{1}, #tilde{#chi}^{+}_{1}#tilde{#chi}^{-}_{1}, #tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{1} (Higgsino)}#bf{m(#tilde{#chi}^{0}_{2}) = m(#tilde{#chi}^{0}_{1}) + 2#Delta m(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})}","L")
    legend0.SetBorderSize(0)
    legend0.SetFillStyle(0)
    legend0.SetTextSize(0.03)
    legend0.SetTextFont(62)  # 62 = Helvetica bold
    dummyObs = ROOT.TH1F("dummyObs","",1,0,1)
    dummyObs.SetLineStyle(1)          
    dummyObs.SetLineColor(ROOT.kBlack)  # black line
    dummyObs.SetLineWidth(2)
    dummyExp = ROOT.TH1F("dummyExp","",1,0,1)
    dummyExp.SetLineStyle(2)            # dashed
    dummyExp.SetLineColor(ROOT.kBlack)  # black line
    dummyExp.SetLineWidth(2)
    legend = ROOT.TLegend(0.635, 0.45-0.035*(len(analyses)-2) -0.06, 0.905, 0.67+0.035*(len(analyses)-2))
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(dummyObs, "Observed Limit", "l")
    legend.AddEntry(dummyExp, "Expected Limit", "l")    
    basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_18Nov2024HLLHCXSEC.root')
    aux_hist = basefile.Get('basehist')
    base_hist = ROOT.TH2F("","",aux_hist.GetXaxis().GetNbins(), aux_hist.GetXaxis().GetBinLowEdge(1),  aux_hist.GetXaxis().GetBinUpEdge(aux_hist.GetXaxis().GetNbins()),100*aux_hist.GetYaxis().GetNbins(), aux_hist.GetYaxis().GetBinLowEdge(1),  ymax)
    matchHistos(base_hist, aux_hist)
    base_hist.GetYaxis().SetRangeUser(0.135,100.0)
    base_hist.GetYaxis().SetNdivisions(505)
    base_hist.GetXaxis().SetNdivisions(505)
    base_hist.GetXaxis().SetLabelSize(0.0425)  
    base_hist.GetYaxis().SetLabelSize(0.0425)
    base_hist.GetXaxis().SetRangeUser(100,250)
    if 'Recursive Jigsaw' in ','.join(list(analyses.keys())): base_hist.GetXaxis().SetRangeUser(100,300)
    base_hist.GetYaxis().SetTitleOffset(0.9)
    base_hist.GetYaxis().SetMoreLogLabels(True)
    base_hist.GetYaxis().SetNoExponent(True)
    if doHLLHC: 
        #base_hist.GetYaxis().SetRangeUser(0.135,4.3)
        base_hist.GetXaxis().SetRangeUser(99,340)   
        base_hist.GetYaxis().SetTitleOffset(1.0)     
    base_hist.GetXaxis().SetTitle('m_{#tilde{#chi}^{#pm}_{1}} [GeV]')
    base_hist.GetYaxis().SetTitle('#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) [GeV]')
    print(base_hist.GetXaxis().GetTitle(), base_hist.GetYaxis().GetTitle())
    first = True  # flag per il primo elemento
    for analysis_name in analysis_names:
        analysis = analyses[analysis_name]
        path, exp, obj, color = analysis
        print('doing', analysis)
        file = ROOT.TFile.Open(path)
        gexp = file.Get(exp)
        gexp.SetLineColor(color)
        gexp.SetLineStyle(ROOT.kDashed)
        gexp.SetLineWidth(3)
        mg.Add(gexp)            
        #legend.AddEntry(gexp, "%s Expected" % analysis_name, "l")            
        if obj=='':
            gobs = None
        else: 
            gobs = file.Get(obj)
            gobs.SetLineColor(color)
            gobs.SetLineWidth(3)
            gobs.SetFillColorAlpha(color, 0.35)
            # a dirty way to fill the are for the first analysis curve
            if first and 'disappearing' in analysis_name.lower():
                first = False
                N = gobs.GetN()
                gobsFilled = ROOT.TGraph(N+2)
                for j in range(N):
                    x_arr = array('d', [0.])
                    y_arr = array('d', [0.])
                    gobs.GetPoint(j, x_arr, y_arr)
                    gobsFilled.SetPoint(j, x_arr[0], y_arr[0])
                # Add two points to close the area
                x_arr = array('d', [0.])
                y_arr = array('d', [0.])
                gobs.GetPoint(N-1, x_arr, y_arr)
                baseline = 0.0  
                gobsFilled.SetPoint(N, x_arr[0], baseline)
                x_arr = array('d', [0.])
                y_arr = array('d', [0.])
                gobs.GetPoint(0, x_arr, y_arr)
                gobsFilled.SetPoint(N+1, x_arr[0], baseline)
                gobsFilled.SetLineColor(color)
                gobsFilled.SetLineWidth(3)
                gobsFilled.SetFillColorAlpha(color, 0.35)
                gobsFilled.SetFillStyle(1001)
                mg.Add(gobsFilled, "LF")
                legend.AddEntry(gobsFilled, "%s" % analysis_name, "f")
            else:
                mg.Add(gobs, "LF")
                #legend.AddEntry(gobs, "%s Observed" % analysis_name, "l")
                legend.AddEntry(gobs, "%s" % analysis_name, "f")
    file.Close()
    canvas.cd()
    canvas.SetLogy()
    base_hist.Draw()
    # needed for change ranges coherently on the MultiGraph
    #mg.SetMinimum(0.2)
    #mg.SetMaximum(50.0)
    #mg.GetXaxis().SetLimits(100,250)  
    #mg.GetYaxis().SetNdivisions(505)
    #mg.GetYaxis().SetTitleOffset(0.8)
    #mg.GetYaxis().SetMoreLogLabels(True)
    #mg.GetYaxis().SetNoExponent(True)
    #mg.GetXaxis().SetTitle('m_{#tilde{#chi}^{#pm}_{1}} [GeV]')
    #mg.GetYaxis().SetTitle('#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) [GeV]')
    #mg.Draw("AL")
    mg.Draw("L")
    legend0.Draw()
    #legend00.Draw() 
    legend.Draw()
    #canvas.SetGrid()
    if drawRadiativeBound:
        fsatoshi = ROOT.TFile('auxiliary/SatoshiDmChipmChi10.root')
        dmrad_chipm_chi10 = fsatoshi.Get('dmrad_chipm_chi10')
        dmrad_chipm_chi10.SetLineColor(ROOT.kRed) #kOrange+2
        dmrad_chipm_chi10.SetLineWidth(2)
        dmrad_chipm_chi10.SetLineStyle(ROOT.kDotted)        
        dmrad_chipm_chi10.Draw('same')
        legend.AddEntry(dmrad_chipm_chi10, "Radiative corrections", "l")
    
    if doHLLHC: 
        stamp(3000)
    else: 
        stamp()
    plotstem = 'summary_ewk_compressed'+'_HLLHC'*doHLLHC
    canvas.SaveAs(plotstem+".pdf")
    canvas.SaveAs(plotstem+".png")

def stamp(lumi='129-138', datamc_ = 'data', showlumi = True, WorkInProgress = False):
    cmsTextFont = 61
    extraTextFont = 50
    lumiTextSize = 0.8 #0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    originalfont = tl.GetTextFont()
    datamc = 'Data'
    datamc = datamc_.lower()
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.1*tl.GetTextSize())
    tl.DrawLatex(0.12,0.85, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(0.75/1.1*tl.GetTextSize())
    xlab = 0.205
    if ('mc' in datamc): thing = 'simulation'
    else: thing = 'Preliminary'
    if WorkInProgress: tl.DrawLatex(xlab,0.91, ' internal')
    else: tl.DrawLatex(xlab,0.85, thing)
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    #if showlumi: thingy+=str(lumi)+' fb^{-1} '+'(13 TeV)'
    if showlumi: thingy = "#scale[1.05]{#bf{" + str(lumi) + " fb^{-1} (13 TeV)}}"  
    xthing = 0.65 #0.65 #0.667
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.73,thingy)
    tl.SetTextSize(1.0/0.7*tl.GetTextSize())
   
def matchHistos(base_hist, aux_hist):    
    xax, yax = aux_hist.GetXaxis(), aux_hist.GetYaxis()
    nx, ny = xax.GetNbins(), yax.GetNbins()
    for m in dir(aux_hist):
        if m.startswith("Get") and hasattr(base_hist, "Set" + m[3:]):
            try: getattr(base_hist, "Set" + m[3:])(getattr(aux_hist, m)())
            except: continue
    for m in dir(xax):
        if m.startswith("Get") and hasattr(base_hist.GetXaxis(), "Set" + m[3:]):
            try: 
                getattr(base_hist.GetXaxis(), "Set" + m[3:])(getattr(xax, m)())
                getattr(base_hist.GetYaxis(), "Set" + m[3:])(getattr(yax, m)())
            except: continue     
main()
