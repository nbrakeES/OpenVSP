# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
#sys.path.append('C:\\OpenVSP_dev\\build_release_vsp\\src\\python_api')
#sys.path.append('C:\\OpenVSP_dev\\build_release_vsp\\src\\python_api\\Release')
sys.path.append('C:\\AeroTools\\OpenVSP_DevBuild')

import vsp

stdout = vsp.cvar.cstdout

print("starting some stuff")

wing_id = vsp.AddGeom( "WING")
vsp.SetGeomName( wing_id, "MainWing" )
vsp.SetParmValUpdate(  wing_id, "TotalSpan", "WingGeom", 17.0 )
vsp.SetParmValUpdate(  wing_id, "Z_Rel_Location", "XForm", 0.5 )
# Adjust chordwise tesselation
# vsp.SetParmValUpdate(  wing_id, "Tess_W", "Shape", 33 )
vsp.SetParmValUpdate(  wing_id, "LECluster", "WingGeom", 0.0 )
vsp.SetParmValUpdate(  wing_id, "TECluster", "WingGeom", 2.0 )
# Adjust spanwise tesselation
# vsp.SetParmValUpdate(  wing_id, "SectTess_U", "XSec_1", 25 )
vsp.SetParmValUpdate(  wing_id, "InCluster", "XSec_1", 0.1 )
vsp.SetParmValUpdate(  wing_id, "OutCluster", "XSec_1", 0.0 )
subsurf_id = vsp.AddSubSurf( wing_id, vsp.SS_CONTROL, 0 )

#printf("\tAdding POD\n")
pod_id = vsp.AddGeom( "POD")
vsp.SetParmValUpdate(  pod_id, "Length", "Design", 14.5 )
vsp.SetParmValUpdate(  pod_id, "X_Rel_Location", "XForm", -3.0 )
vsp.SetParmValUpdate(  wing_id, "Tess_U", "Shape", 25 ) #lengthwise tesselation
vsp.SetParmValUpdate(  wing_id, "Tess_W", "Shape", 25 ) #radial tesselation

#printf("\tAdding DISK\n")
disk_id = vsp.AddGeom( "DISK")
vsp.SetParmValUpdate(  disk_id, "Diameter", "Design", 3.0 )
vsp.SetParmValUpdate(  disk_id, "Y_Rel_Location", "XForm", 3.5 )

# Add tail with X-axis symetry and 3 total surfaces (Y-Tail configuration)
#printf("\tAdding WING (Tail)\n")
wing2_id = vsp.AddGeom( "WING")
vsp.SetGeomName( wing2_id, "Tail" )
vsp.SetParmValUpdate(  wing2_id, "X_Rel_Location", "XForm", 9.0 )
vsp.SetParmValUpdate(  wing2_id, "X_Rel_Rotation", "XForm", 30.0 )
vsp.SetParmValUpdate(  wing2_id, "TotalSpan", "WingGeom", 5.0 )
vsp.SetParmValUpdate(  wing2_id, "LECluster", "WingGeom", 0.0 )
vsp.SetParmValUpdate(  wing2_id, "TECluster", "WingGeom", 2.0 )
# vsp.SetParmValUpdate(  wing2_id, "SectTess_U", "XSec_1", 25 )
vsp.SetParmValUpdate(  wing2_id, "InCluster", "XSec_1", 0.1 )
vsp.SetParmValUpdate(  wing2_id, "OutCluster", "XSec_1", 0.0 )
# change symetry for tail to make Y shape tail
vsp.SetParmValUpdate(  wing2_id, "Sym_Planar_Flag", "Sym", 0 ) #no planar symetry
vsp.SetParmValUpdate(  wing2_id, "Sym_Axial_Flag", "Sym", vsp.SYM_ROT_X ) # X-a
vsp.SetParmValUpdate(  wing2_id, "Sym_Rot_N", "Sym", 3 ) #no planar symetry

#TODO Organize geometry into sets: 1 setf for VLM and 1 set for panel

vsp.Update() 
#vsp.ErrorMgr().PopErrorAndPrint( stdout )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE

#==== Setup export filenames ====#
# Execution of one of these methods is required to propperly set the export filenames for creation of vspaero input files and execution commands
m_vspfname_for_vspaerotests = "apitest_TestVSPAero.vsp3"
vsp.SetVSP3FileName( m_vspfname_for_vspaerotests )  # this still needs to be done even if a call to WriteVSPFile is made
vsp.Update()

#==== Save Vehicle to File ====#
vsp.WriteVSPFile( vsp.GetVSPFileName(), vsp.SET_ALL )

# Final check for errors
#vsp.ErrorMgr.PopErrorAndPrint( stdout )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE

#open the file created in TestVSPAeroCreateModel
vsp.ReadVSPFile( m_vspfname_for_vspaerotests )

#==== Analysis: VSPAero Compute Geometry ====#
analysis_name = "VSPAEROComputeGeometry"
#printf("\t%s\n",analysis_name.c_str())

# Set defaults
vsp.SetAnalysisInputDefaults(analysis_name)

# list inputs, type, and current values
vsp.PrintAnalysisInputs(stdout,analysis_name)

# Execute
#printf("\tExecuting...\n")
results_id = vsp.ExecAnalysis(analysis_name)
#printf("COMPLETE\n")

# Get & Display Results
vsp.PrintResults(stdout, results_id )

# Final check for errors
#vsp.ErrorMgr.PopErrorAndPrint( stdout )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE
#printf("\n")


##==== Analysis: VSPAERO Sweep ====#
#analysis_name = "VSPAEROSweep"
##printf("\t%s\n",analysis_name.c_str())
## Set defaults
#vsp.SetAnalysisInputDefaults(analysis_name)
#
## Change some input values
##    Reference geometry set
#vsp.SetIntAnalysisInput(analysis_name, "GeomSet", [vsp.SET_ALL])
##    Reference areas, lengths
#sref = 10
#vsp.SetDoubleAnalysisInput(analysis_name, "Sref", [10])
#bref = 17
#vsp.SetDoubleAnalysisInput(analysis_name, "bref", [17])
#cref = 3
#vsp.SetDoubleAnalysisInput(analysis_name, "cref", [3])
#ref_flag = 3
#vsp.SetIntAnalysisInput(analysis_name, "RefFlag", [3])
##    freestream parameters
##        Alpha
#alpha_start = [5]
#alpha_end = [10]
#alpha_npts = [1]
#vsp.SetDoubleAnalysisInput(analysis_name, "AlphaStart", alpha_start)
#vsp.SetDoubleAnalysisInput(analysis_name, "AlphaEnd", alpha_end)
#vsp.SetIntAnalysisInput(analysis_name, "AlphaNpts", alpha_npts)
##        Beta
#beta_start = [0]
#beta_end = [0]
#beta_npts = [1]
#vsp.SetDoubleAnalysisInput(analysis_name, "BetaStart", beta_start)
#vsp.SetDoubleAnalysisInput(analysis_name, "BetaEnd", beta_end)
#vsp.SetIntAnalysisInput(analysis_name, "BetaNpts", beta_npts)
##        Mach
#mach_start = [0]
#mach_end = [0]
#mach_npts = [1]
#vsp.SetDoubleAnalysisInput(analysis_name, "MachStart", mach_start)
#vsp.SetDoubleAnalysisInput(analysis_name, "MachEnd", mach_end)
#vsp.SetIntAnalysisInput(analysis_name, "MachNpts", mach_npts)
##        Set Batch Mode
#batch_mode_flag = [1]
#vsp.SetIntAnalysisInput(analysis_name, "BatchModeFlag", batch_mode_flag)
#
#vsp.Update()
##vsp.ErrorMgr.PopErrorAndPrint( stdout ) )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE
#
## list inputs, type, and current values
#vsp.PrintAnalysisInputs(stdout,analysis_name)
#
## Execute
##printf("\tExecuting...\n")
#results_id = vsp.ExecAnalysis(analysis_name)
##printf("COMPLETE\n")
##vsp.ErrorMgr.PopErrorAndPrint( stdout ) )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE
#
## Get & Display Results
#vsp.PrintResults(stdout, results_id )
#
## Final check for errors
##vsp.ErrorMgr.PopErrorAndPrint( stdout ) )    #PopErrorAndPrint returns TRUE if there is an error we want ASSERT to check that this is FALSE
##printf("\n")
#exit()