from flightdata import Flight, Fields, CIDTypes
bin=Flight.from_log('./logs/00000100.BIN')

print(bin.subset(100, 101).read_fields([Fields.POSITION, Fields.ATTITUDE]))

