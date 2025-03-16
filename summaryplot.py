import ROOT
ROOT.gROOT.SetBatch(1)
import os

tl = ROOT.TLatex()
tl.SetNDC()

doHLLHC = False
    
def main():
    analyses = {}
    analyses['Disappearing Tracks'] = ['results_sus_21_006/PureHiggsino_DTRun2_results.root', 'Exp_PureHiggsino_DTRun2', 'Obs_PureHiggsino_DTRun2', ROOT.kSpring+2]
    analyses['Isolated soft Track'] = ['results_sus_24_012/PureHiggsino_SDPRun2_results.root', 'Exp_PureHiggsino_SDPRun2', 'Obs_PureHiggsino_SDPRun2', ROOT.kOrange-1]
    #analyses['SUS-24-003'] = ['results_sus_24_003/PureHiggsino_spdl_Run2comb_results.root', 'Exp_PureHiggsino_spdl_comb', 'Obs_PureHiggsino_spdl_comb', ROOT.kRed]
    analyses['Soft 2l and 3l'] = ['results_exo_23_017/h2lim_20250226_Hino_neg_allEEMM_neg_0.0_log_smooth1k5a_dMc1n1.root', 'limitGraph_0', 'limitGraph_obs', ROOT.kAzure-9]
    cadis = list(analyses.keys())
    cadis.reverse()
    if doHLLHC:
        for cadi in cadis:
            analysis = analyses[cadi]
            analysis[0] = analysis[0].replace('Run2','HLLHC')
            analysis[2] = ''
                
    canvas = ROOT.TCanvas("c1", "SUSY EW Summary Plot", 800, 600)
    print(canvas.GetTopMargin(), canvas.GetBottomMargin())
    canvas.SetBottomMargin(0.15)
    canvas.SetTopMargin(1.3)
    
    mg = ROOT.TMultiGraph()
    legend0 = ROOT.TLegend(0.15, 0.70, 0.45, 0.95)
    legend0.SetHeader("#splitline{#bf{pp #rightarrow #chi^{0}_{2}#chi^{#pm}_{1} #chi^{0}_{2}#chi^{#mp}_{1} #chi^{+}_{1}#chi^{-}_{1} #chi^{#mp}_{1}#chi^{0}_{1} (Higgsino)}}{#bf{m(#chi^{0}_{2}) = m(#chi^{0}_{1}) + 2#Delta m(#chi^{#pm}_{1}, #chi^{0}_{1})}}","C")
    legend0.SetBorderSize(0)
    legend0.SetFillStyle(0)
    legend0.SetTextSize(0.03)
    dummyObs = ROOT.TH1F("dummyObs","",1,0,1)
    dummyObs.SetLineStyle(1)          
    dummyObs.SetLineColor(ROOT.kBlack)  # black line
    dummyObs.SetLineWidth(2)
    dummyExp = ROOT.TH1F("dummyExp","",1,0,1)
    dummyExp.SetLineStyle(2)            # dashed
    dummyExp.SetLineColor(ROOT.kBlack)  # black line
    dummyExp.SetLineWidth(2)
    #dummyExp.SetFillColor(ROOT.kYellow) # yellow fill
    #dummyExp.SetFillStyle(1001)         # solid fill
    legend00 = ROOT.TLegend(0.61, 0.45, 0.88, 0.60)
    legend00.SetHeader("All limits at 95% CL", "L")  
    #legend00.AddEntry(dummyObs, "Observed Limit (#pm 1#sigma^{SUSY}_{theory})", "l")
    #legend00.AddEntry(dummyExp, "Expected Limit (#pm 1#sigma^{exp})", "lf")
    legend00.AddEntry(dummyObs, "Observed Limit", "l")
    legend00.AddEntry(dummyExp, "Expected Limit", "l")
    legend00.SetBorderSize(0)
    legend00.SetFillStyle(0)
    legend00.SetTextSize(0.03)
    legend = ROOT.TLegend(0.61, 0.28-0.07*(len(analyses)-3), 0.88, 0.43) #0.53
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_18Nov2024HLLHCXSEC.root')
    #else: basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_25Nov2024Observed4thabaseXSEC.root')
    base_hist = basefile.Get('basehist')
    base_hist.GetYaxis().SetRangeUser(0.2,5.0)
    base_hist.GetYaxis().SetNdivisions(505)
    base_hist.GetXaxis().SetRangeUser(100,250)
    base_hist.GetYaxis().SetTitleOffset(0.8)
    base_hist.GetYaxis().SetMoreLogLabels(True)
    base_hist.GetYaxis().SetNoExponent(True)
    if doHLLHC: 
        #base_hist.GetYaxis().SetRangeUser(0.135,4.3)
        base_hist.GetXaxis().SetRangeUser(99,340)   
        base_hist.GetYaxis().SetTitleOffset(1.0)     
    base_hist.GetXaxis().SetTitle('m_{#tilde{#chi}^{#pm}_{1}} [GeV]')
    base_hist.GetYaxis().SetTitle('#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) [GeV]')
    print(base_hist.GetXaxis().GetTitle(), base_hist.GetYaxis().GetTitle())
    for cadi in cadis:
        analysis = analyses[cadi]
        path, exp, obj, color = analysis
        print('doing', analysis)
        file = ROOT.TFile.Open(path)
        gexp = file.Get(exp)
        gexp.SetLineColor(color)
        gexp.SetLineStyle(ROOT.kDashed)
        gexp.SetLineWidth(3)
        mg.Add(gexp)            
        #legend.AddEntry(gexp, "%s Expected" % cadi, "l")            
        if obj=='': gobs = None
        else: 
            gobs = file.Get(obj)
            gobs.SetLineColor(color)
            #gobs.SetLineStyle(1)
            gobs.SetLineWidth(3)
            gobs.SetFillColorAlpha(color, 0.35)
            mg.Add(gobs, "LF")
            #legend.AddEntry(gobs, "%s Observed" % cadi, "l")
            legend.AddEntry(gobs, "%s" % cadi, "f")
        file.Close()
    canvas.cd()
    canvas.SetLogy()
    base_hist.Draw()
    mg.Draw("L")
    legend0.Draw()
    legend00.Draw() 
    legend.Draw()
    #canvas.SetLogy()
    #canvas.SetGrid()
    if doHLLHC: stamp(3000)
    else: stamp()
    plotstem = 'summary_ewk_compressed'+'_HLLHC'*doHLLHC
    canvas.SaveAs(plotstem+".pdf")
    canvas.SaveAs(plotstem+".png")
    print ("Summary plot saved as {plotstem}'.pdf'")

def stamp(lumi='129-138', datamc_ = 'data', showlumi = True, WorkInProgress = False):
    cmsTextFont = 61
    extraTextFont = 50
    lumiTextSize = 0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    originalfont = tl.GetTextFont()
    datamc = 'Data'
    datamc = datamc_.lower()
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.98*tl.GetTextSize())
    tl.DrawLatex(0.12,0.91, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.98*tl.GetTextSize())
    xlab = 0.2
    if ('mc' in datamc): thing = 'simulation'
    else: thing = 'preliminary'
    if WorkInProgress: tl.DrawLatex(xlab,0.91, ' internal')
    else: tl.DrawLatex(xlab,0.91, thing)
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+=str(lumi)+' fb^{-1} '+'(13 TeV)'
    xthing = 0.65 #0.667
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.91,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())
    
main()
