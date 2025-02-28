import ROOT
ROOT.gROOT.SetBatch(1)
import os

tl = ROOT.TLatex()
tl.SetNDC()

doHLLHC = False
    
def main():
    analyses = {}
    analyses['SUS-21-006'] = ['results_sus_21_006/PureHiggsino_DTRun2_results.root', 'Exp_PureHiggsino_DTRun2', 'Obs_PureHiggsino_DTRun2', ROOT.kRed]
    analyses['SUS-24-012'] = ['results_sus_24_012/PureHiggsino_SDPRun2_results.root', 'Exp_PureHiggsino_SDPRun2', 'Obs_PureHiggsino_SDPRun2', ROOT.kBlue]
    analyses['SUS-24-003'] = ['results_sus_24_003/PureHiggsino_spdl_Run2comb_results.root', 'Exp_PureHiggsino_spdl_comb', 'Obs_PureHiggsino_spdl_comb', ROOT.kGreen + 2]
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
    canvas.SetTopMargin(0.05)
    
    mg = ROOT.TMultiGraph()
    legend = ROOT.TLegend(0.61, 0.63-0.07*(len(analyses)-3), 0.88, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_18Nov2024HLLHCXSEC.root')
    #else: basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_25Nov2024Observed4thabaseXSEC.root')
    base_hist = basefile.Get('basehist')
    base_hist.GetYaxis().SetRangeUser(0.135,4.0)
    base_hist.GetXaxis().SetRangeUser(99,210)    
    if doHLLHC: 
        base_hist.GetYaxis().SetRangeUser(0.135,5.2)
        base_hist.GetXaxis().SetRangeUser(99,310)   
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
        legend.AddEntry(gexp, "%s Expected" % cadi, "l")            
        if obj=='': gobs = None
        else: 
            gobs = file.Get(obj)
            gobs.SetLineColor(color)
            #gobs.SetLineStyle(1)
            gobs.SetLineWidth(3)
            mg.Add(gobs, "L")
            legend.AddEntry(gobs, "%s Observed" % cadi, "l")
        file.Close()
    canvas.cd()
    base_hist.Draw()
    mg.Draw("L")
    legend.Draw()
    #canvas.SetLogy()
    #canvas.SetGrid()
    if doHLLHC: stamp(3000)
    else: stamp()
    plotstem = 'summary_ewk_compressed'+'_HLLHC'*doHLLHC
    canvas.SaveAs(plotstem+".pdf")
    canvas.SaveAs(plotstem+".png")
    print ("Summary plot saved as {plotstem}'.pdf'")

def stamp(lumi='138', datamc_ = 'data', showlumi = True, WorkInProgress = False):
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
    tl.DrawLatex(0.12,0.9, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.98*tl.GetTextSize())
    xlab = 0.2
    if ('mc' in datamc): thing = 'simulation'
    else: thing = 'preliminary'
    if WorkInProgress: tl.DrawLatex(xlab,0.9, ' internal')
    else: tl.DrawLatex(xlab,0.9, thing)
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+=str(lumi)+' fb^{-1} '+'(13 TeV)'
    xthing = 0.667
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.9,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())
    
main()
