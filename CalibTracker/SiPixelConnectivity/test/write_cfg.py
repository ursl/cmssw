import FWCore.ParameterSet.Config as cms

process = cms.Process("MapWriter")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.CondDBCommon.connect = cms.string("sqlite_file:cabling.db")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.CMSCommonData.cmsExtendedGeometry2015PilotXML_cfi")
process.trackerGeometry.applyAlignment = cms.bool(False)
 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

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
        tag = cms.string('SiPixelFedCablingMap_v20')
    )),
    loadBlobStreamer = cms.untracked.bool(False)
)

#process.MessageLogger = cms.Service("MessageLogger",
#    debugModules = cms.untracked.vstring('*'),
#    destinations = cms.untracked.vstring('out'),
#    out = cms.untracked.PSet( threshold = cms.untracked.string('DEBUG'))
#)

process.load("CalibTracker.SiPixelConnectivity.PixelToLNKAssociateFromAsciiESProducer_cfi")

#ul changes
process.GlobalTag.globaltag = 'START70_V7A::All'
process.pixelToLNKAssociateFromAscii.fileName = cms.string('pixelToLNK_pilot.ascii')

process.mapwriter = cms.EDAnalyzer("SiPixelFedCablingMapWriter",
  record = cms.string('SiPixelFedCablingMapRcd'),
  associator = cms.untracked.string('PixelToLNKAssociateFromAscii')
)

process.p1 = cms.Path(process.mapwriter)
