import FWCore.ParameterSet.Config as cms

process = cms.Process("MapWriter")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.CondDBCommon.connect = cms.string("sqlite_file:cabling.db")

 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# requires >= CMSSW_7_4_10
process.GlobalTag.globaltag = "74X_dataRun2_Prompt_v2"

# ---------------------- pilotBlade Geometry -------------------
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
# -- would like to get this to work ...
#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load("Geometry.CMSCommonData.cmsExtendedGeometry2015PilotXML_cfi")
process.trackerGeometryDB.applyAlignment = cms.bool(False)
process.XMLFromDBSource.label=''
process.PoolDBESSourceGeometry = cms.ESSource("PoolDBESSource",
        process.CondDBSetup,
        timetype = cms.string('runnumber'),
        toGet = cms.VPSet(
                cms.PSet(
                        record = cms.string('GeometryFileRcd'),
                        tag = cms.string('XMLFILE_Geometry_74YV2_Extended2015_mc')
                ),
                cms.PSet(
                        record = cms.string('IdealGeometryRecord'),
                        tag = cms.string('TKRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PGeometricDetExtraRcd'),
                        tag = cms.string('TKExtra_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PTrackerParametersRcd'),
                        tag = cms.string('TKParameters_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PEcalBarrelRcd'),
                        tag = cms.string('EBRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PEcalEndcapRcd'),
                        tag = cms.string('EERECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PEcalPreshowerRcd'),
                        tag = cms.string('EPRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PHcalRcd'),
                        tag = cms.string('HCALRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PCaloTowerRcd'),
                        tag = cms.string('CTRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PZdcRcd'),
                        tag = cms.string('ZDCRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('PCastorRcd'),
                        tag = cms.string('CASTORRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('CSCRecoGeometryRcd'),
                        tag = cms.string('CSCRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('CSCRecoDigiParametersRcd'),
                        tag = cms.string('CSCRECODIGI_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('DTRecoGeometryRcd'),
                        tag = cms.string('DTRECO_Geometry_74YV2')
                ),
                cms.PSet(
                        record = cms.string('RPCRecoGeometryRcd'),
                        tag = cms.string('RPCRECO_Geometry_74YV2')
                )
        ),
        connect = cms.string('sqlite_file:./PilotGeometry.db') 
)
process.es_prefer_geometry = cms.ESPrefer( "PoolDBESSource", "PoolDBESSourceGeometry" )
#-------------------------------------------------------



process.source = cms.Source("EmptyIOVSource",
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    interval = cms.uint64(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBCommon,
    toPut = cms.VPSet(cms.PSet(
        record =  cms.string('SiPixelFedCablingMapRcd'),
        tag = cms.string('SiPixelFedCablingMap_v21')
    )),
    loadBlobStreamer = cms.untracked.bool(False)
)

#process.MessageLogger = cms.Service("MessageLogger",
#    debugModules = cms.untracked.vstring('*'),
#    destinations = cms.untracked.vstring('out'),
#    out = cms.untracked.PSet( threshold = cms.untracked.string('DEBUG'))
#)

process.load("CalibTracker.SiPixelConnectivity.PixelToLNKAssociateFromAsciiESProducer_cfi")

process.pixelToLNKAssociateFromAscii.fileName = cms.string('pixelToLNK_pilot_V21.ascii')

process.mapwriter = cms.EDAnalyzer("SiPixelFedCablingMapWriter",
  record = cms.string('SiPixelFedCablingMapRcd'),
  associator = cms.untracked.string('PixelToLNKAssociateFromAscii')
)

process.p1 = cms.Path(process.mapwriter)
