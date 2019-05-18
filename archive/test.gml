graph [
  DateObtained "2/12/10"
  GeoLocation "Australia"
  GeoExtent "Country"
  Network "AARNET"
  Provenance "Primary"
  Access 0
  Source "http://www.aarnet.edu.au/aarnet3.aspx"
  Version "1.0"
  Type "REN"
  DateType "Current"
  Backbone 1
  Commercial 0
  label "Aarnet"
  ToolsetVersion "0.3.34dev-20120328"
  Customer 0
  IX 0
  SourceGitVersion "e278b1b"
  DateModifier "="
  DateMonth "08"
  LastAccess "3/08/10"
  Layer "IP"
  Creator "Topology Zoo Toolset"
  Developed 1
  Transit 0
  NetworkDate "2010_08"
  DateYear "2010"
  LastProcessed "2011_09_01"
  Testbed 0
  node [
    id 0
    label "Sydney1"
    Country "Australia"
    Longitude 151.20732
    Internal 1
    Latitude -33.86785
  ]
  node [
    id 1
    label "Brisbane2"
    Country "Australia"
    Longitude 153.02809
    Internal 1
    Latitude -27.46794
  ]
  node [
    id 2
    label "Canberra1"
    Country "Australia"
    Longitude 149.12807
    Internal 1
    Latitude -35.28346
  ]
  node [
    id 3
    label "Sydney2"
    Country "Australia"
    Longitude 151.20732
    Internal 1
    Latitude -33.86785
  ]
  node [
    id 4
    label "Townsville"
    Country "Australia"
    Longitude 146.8
    Internal 1
    Latitude -19.25
  ]
  node [
    id 5
    label "Cairns"
    Country "Australia"
    Longitude 145.76667
    Internal 1
    Latitude -16.91667
  ]
  edge [
    source 1
    target 3
    LinkLabel "< 10 Gbps"
  ]
  edge [
    source 2
    target 3
    LinkLabel "< 10 Gbps"
  ]
  edge [
    source 3
    target 4
    LinkLabel "< 10 Gbps"
  ]
  edge [
    source 4
    target 5
    LinkLabel "< 10 Gbps"
  ]
  edge [
    source 4
    target 6
    LinkLabel "< 10Gbps"
  ]
]
