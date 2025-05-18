import ROOT
ROOT.gROOT.SetBatch(1)
import os
from array import array
ROOT.gStyle.SetOptStat(0)

tl = ROOT.TLatex()
tl.SetNDC()

doHLLHC = True
drawRadiativeBound = True
UseYR2018 = True

def main():
    analyses = {
        '#splitline{Disappearing Track}{arXiv:2309.16823}': {
            'Run2': {
                'file':  'results_sus_21_006/PureHiggsino_DTRun2_results.root',
                'exp':   'Exp_PureHiggsino_DTRun2',
                'obs':   'Obs_PureHiggsino_DTRun2',
                'color': ROOT.kSpring+2,
                'style': 1
            },
            '400fb': {
                'file':  'results_sus_21_006/PureHiggsino_DTRun2_results400infb.root',
                'exp':   'Exp_PureHiggsino_DTRun2',
                'obs':   None,
                'color': ROOT.kSpring+2,
                'style': 7
            },
            '3000fb': {
                'file':  'results_sus_21_006/PureHiggsino_DTRun2_results3000infb.root',
                'exp':   'Exp_PureHiggsino_DTRun2',
                'obs':   None,
                'color': ROOT.kSpring+2,
                'style': 5
            },
            '6000fb': {
                'file':  'results_sus_21_006/PureHiggsino_DTRun2_results6000infb.root',
                'exp':   'Exp_PureHiggsino_DTRun2',
                'obs':   None,
                'color': ROOT.kSpring+2,
                'style': 8
            },            
        },
        '#splitline{Isolated Soft Track}{SUS-24-012}': {
            'Run2': {
                'file':  'results_sus_24_012/PureHiggsino_SDPRun2_results.root',
                'exp':   'Exp_PureHiggsino_SDPRun2',
                'obs':   'Obs_PureHiggsino_SDPRun2',
                'color': ROOT.kOrange-1,
                'style': 1
            },
            '400fb': {
                'file':  'results_sus_24_012/PureHiggsino_SDPRun2_results400infb.root',
                'exp':   'Exp_PureHiggsino_SDPRun2',
                'obs':   None,
                'color': ROOT.kOrange-1,
                'style': 7
            },
            '3000fb': {
                'file':  'results_sus_24_012/PureHiggsino_SDPRun2_results3000infb.root',
                'exp':   'Exp_PureHiggsino_SDPRun2',
                'obs':   None,
                'color': ROOT.kOrange-1,
                'style': 5
            },
            '6000fb': {
                'file':  'results_sus_24_012/PureHiggsino_SDPRun2_results6000infb.root',
                'exp':   'Exp_PureHiggsino_SDPRun2',
                'obs':   None,
                'color': ROOT.kOrange-1,
                'style': 8
            },
        },
        '#splitline{Soft 2l and 3l}{EXO-23-017}': {
            'Run2': {
                'file':  'results_exo_23_017/h2lim_20250226_Hino_neg_allEEMM_neg_0.0_log_smooth1k5a_dMc1n1.root',
                'exp':   'limitGraph_0',
                'obs':   'limitGraph_obs',
                'color': ROOT.kAzure-9,
                'style': 1
            }
        },
    }

    all_labels = list(analyses.keys())

    # Decide axis range
    if 'Recursive Jigsaw' in ','.join(all_labels):
        xmax, ymax = 300, 100
    else:
        xmax, ymax = 480, 8

    # Reverse so the last one in dictionary is drawn on top
    all_labels.reverse()

    canvas = ROOT.TCanvas("c1", "SUSY EW Summary Plot", 800, 600)
    canvas.SetBottomMargin(0.15)
    canvas.SetTopMargin(1.3)
    mg = ROOT.TMultiGraph()

    legend = ROOT.TLegend(0.61, 0.45 - 0.035*(len(all_labels)-2) - 0.06,
                          0.9, 0.85 + 0.035*(len(all_labels)-2))
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)    

    legend0 = ROOT.TLegend(0.12, 0.64, 0.30, 0.89)
    legend0.SetHeader("#splitline{#bf{pp#rightarrow#tilde{#chi}^{0}_{2}#tilde{#chi}^{#pm}_{1}, "
                      "#tilde{#chi}^{0}_{2}#tilde{#chi}^{0}_{1}, #tilde{#chi}^{+}_{1}#tilde{#chi}^{-}_{1}, "
                      "#tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{1} (Higgsino)}}"
                      "{#bf{m(#tilde{#chi}^{0}_{2}) = m(#tilde{#chi}^{0}_{1}) + "
                      "2#Delta m(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})}}","L")
    legend0.SetBorderSize(0)
    legend0.SetFillStyle(0)
    legend0.SetTextSize(0.03)
    legend0.SetTextFont(62)

    basefile = ROOT.TFile.Open('results_sus_24_003/PureHiggsino_SoftPromptRun2_18Nov2024HLLHCXSEC.root')
    aux_hist = basefile.Get('basehist')
    base_hist = ROOT.TH2F("", "", 
                          100*aux_hist.GetXaxis().GetNbins(),
                          aux_hist.GetXaxis().GetBinLowEdge(1),
                          xmax,
                          100*aux_hist.GetYaxis().GetNbins(),
                          aux_hist.GetYaxis().GetBinLowEdge(1),
                          ymax)
    matchHistos(base_hist, aux_hist)
    base_hist.GetYaxis().SetRangeUser(0.135, 100.0)
    base_hist.GetYaxis().SetNdivisions(505)
    base_hist.GetXaxis().SetNdivisions(505)
    base_hist.GetXaxis().SetLabelSize(0.0425)
    base_hist.GetYaxis().SetLabelSize(0.0425)
    base_hist.GetXaxis().SetRangeUser(99, xmax)
    base_hist.GetYaxis().SetTitleOffset(0.9)
    base_hist.GetYaxis().SetMoreLogLabels(True)
    base_hist.GetYaxis().SetNoExponent(True)

    if doHLLHC:
        base_hist.GetXaxis().SetRangeUser(99, xmax)
        base_hist.GetYaxis().SetTitleOffset(1.0)

    base_hist.GetXaxis().SetTitle('m_{#tilde{#chi}^{#pm}_{1}} [GeV]')
    base_hist.GetYaxis().SetTitle('#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) [GeV]')

    #map to track which scenario-luminosities exist (besides Run2).
    scenario_lines = {}
    
    first = True  # flag per il primo elemento
    for analysis_name in all_labels:
        scenarios = analyses[analysis_name]

        for scenario_name, scenario_dict in scenarios.items():
            path  = scenario_dict['file']
            exp   = scenario_dict['exp']
            obs   = scenario_dict['obs']
            color = scenario_dict['color']
            lstyle= scenario_dict['style']

            if scenario_name != 'Run2': scenario_lines[scenario_name] = lstyle
            if UseYR2018:
                
                path = path.replace('infb.root','infb_YR2018.root')
                
                print('replaced, so', path)

            f = ROOT.TFile.Open(path)
            
            gexp = f.Get(exp)
            if gexp:
                gexp.SetLineColor(color)
                gexp.SetLineStyle(ROOT.kDashed if scenario_name == 'Run2' else lstyle)
                gexp.SetLineWidth(3)
                mg.Add(gexp, "L")

            if obs:
                gobs = f.Get(obs)
                if gobs:
                    
                    gobs.SetLineColor(color)
                    gobs.SetLineWidth(3)
                    gobs.SetLineStyle(1)
                    gobs.SetFillColorAlpha(color, 0.35)
                    if first: 
                        N = gobs.GetN()
                        gobsFilled = ROOT.TGraph(N+2)
                        for j in range(N):
                            x_arr, y_arr = array('d',[0.]), array('d',[0.])
                            gobs.GetPoint(j, x_arr, y_arr)
                            gobsFilled.SetPoint(j, x_arr[0], y_arr[0])
                        # close area to something slightly above 0 so it's visible
                        y_fill_bottom = 0.135
                        x_arr, y_arr = array('d',[0.]), array('d',[0.])
                        gobs.GetPoint(N-1, x_arr, y_arr)
                        gobsFilled.SetPoint(N, x_arr[0], y_fill_bottom)
                        x_arr, y_arr = array('d',[0.]), array('d',[0.])
                        gobs.GetPoint(0, x_arr, y_arr)
                        gobsFilled.SetPoint(N+1, x_arr[0], y_fill_bottom)

                        gobsFilled.SetLineColor(color)
                        gobsFilled.SetLineWidth(3)
                        gobsFilled.SetFillColorAlpha(color, 0.35)
                        gobsFilled.SetFillStyle(1001)
                        mg.Add(gobsFilled, "LF")
                        legend.AddEntry(gobsFilled, "%s" % (analysis_name), "f")
                        first = True#ok keeping as true
                    else:
                        mg.Add(gobs, "LF")
                        legend.AddEntry(gobs, "%s (%s)" % (analysis_name, scenario_name), "f")

            f.Close()

    dummyObs = ROOT.TH1F("dummyObs","",1,0,1)
    dummyObs.SetLineStyle(1)
    dummyObs.SetLineColor(ROOT.kBlack)
    dummyObs.SetLineWidth(2)
    dummyObs.SetFillStyle(1001)
    dummyObs.SetFillColor(ROOT.kGray)    
    dummyExp = ROOT.TH1F("dummyExp","",1,0,1)
    dummyExp.SetLineStyle(2)
    dummyExp.SetLineColor(ROOT.kBlack)
    dummyExp.SetLineWidth(2)
    legend.AddEntry(dummyObs, "Observed Limit 138 fb^{-1}", "lf")
    legend.AddEntry(dummyExp, "Expected Limit 138 fb^{-1}", "l")
    
    dummies = []
    for sc_name in scenario_lines.keys():
        if 'fb' in sc_name:
            label = sc_name.replace('fb','')
            label += ' fb^{-1}'
        else: label = sc_name
        print('setting', 'Expected '+label, sc_name, scenario_lines[sc_name])
        d = ROOT.TH1F("dummy_"+sc_name, "", 1, 0, 1)
        dummies.append(d)
        dummies[-1].SetLineWidth(3)
        dummies[-1].SetLineStyle(scenario_lines[sc_name])
        dummies[-1].SetLineColor(ROOT.kGray+2)
        legend.AddEntry(d, 'Expected '+label, "l") 
        
    canvas.cd()
    canvas.SetLogy()
    base_hist.Draw()
    mg.Draw("L")
    legend0.Draw()
    legend.Draw()


    if drawRadiativeBound:
        fsatoshi = ROOT.TFile('auxiliary/SatoshiDmChipmChi10.root')
        dmrad_chipm_chi10 = fsatoshi.Get('dmrad_chipm_chi10')
        dmrad_chipm_chi10.SetLineColor(ROOT.kRed)
        dmrad_chipm_chi10.SetLineWidth(2)
        dmrad_chipm_chi10.SetLineStyle(ROOT.kDotted-1)
        dmrad_chipm_chi10.Draw('same')
        legend.AddEntry(dmrad_chipm_chi10, "Radiative corrections", "l")

    if doHLLHC:
        tl.SetTextSize(0.5*tl.GetTextSize())
        if UseYR2018: tl.DrawLatex(0.4,0.85,'with YR18 syst. uncert.')
        else: tl.DrawLatex(0.4,0.85,'with Run 2 syst. uncert.')
        tl.SetTextSize(2*tl.GetTextSize())  
        stamp('','data',False)
    else:
        stamp()

    plotstem = 'summary_ewk_projections'
    if doHLLHC:
        if UseYR2018: plotstem += '_YR2018'
        else: plotstem += '_HLLHC'
    canvas.SaveAs(plotstem+".pdf")
    canvas.SaveAs(plotstem+".png")

def stamp(lumi='129-138', datamc_='data', showlumi=True):
    cmsTextFont = 61
    extraTextFont = 50
    regularfont = 42
    datamc = datamc_.lower()
    original_size = tl.GetTextSize()
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.1 * original_size)
    tl.DrawLatex(0.12, 0.85, 'CMS')

    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(0.75/1.1 * original_size)
    xlab = 0.205
    thing = 'simulation' if ('mc' in datamc) else 'Preliminary'
    tl.DrawLatex(xlab, 0.85, thing)

    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81 * tl.GetTextSize())
    if showlumi:
        thingy = "#scale[1.05]{#bf{" + str(lumi) + " fb^{-1} (13 TeV)}}"
        xthing = 0.65
        tl.DrawLatex(xthing, 0.73, thingy)

def matchHistos(base_hist, aux_hist):
    xax, yax = aux_hist.GetXaxis(), aux_hist.GetYaxis()
    for m in dir(aux_hist):
        if m.startswith("Get") and hasattr(base_hist, "Set" + m[3:]):
            try:
                getattr(base_hist, "Set" + m[3:])(getattr(aux_hist, m)())
            except:
                pass
    for m in dir(xax):
        if m.startswith("Get") and hasattr(base_hist.GetXaxis(), "Set" + m[3:]):
            try:
                getattr(base_hist.GetXaxis(), "Set" + m[3:])(getattr(xax, m)())
                getattr(base_hist.GetYaxis(), "Set" + m[3:])(getattr(yax, m)())
            except:
                pass

if __name__=="__main__":
    main()
