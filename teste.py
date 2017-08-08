import math, time

latz = 15 # nz
nb = [19,17] # 0 for surface, 1 for airborne
evenlist = {}
oddlist = {}

nl_table = None
lat_boundaries = [0]*(4*latz-1 + 1)

def calc_lat_boundaries():
	global lat_boundaries

	lat_boundaries[1] = 90
	for i in xrange(2,4*latz-1 + 1):
		lat_boundaries[i] = int(round((180/math.pi) * math.acos(math.sqrt((1-math.cos(math.pi/(2.*15)))/(1-math.cos(2*math.pi/i))))))

def calc_nl_table():
	global nl_table, lat_boundaries

	if nl_table is None:
		nl_table = [0] * 91

		for declat_in in lat_boundaries[1:]:
			for j in range(declat_in,0,-1):
				if j >= 87 or j == 0:
					continue
				nl_table[j] = int(math.floor( (2.0*math.pi) / math.acos(1.0 - (1.0-math.cos(math.pi/(2.0*latz))) / math.cos( (math.pi/180.0)*abs(j) )**2 )))
				assert nl_table[j] in xrange(1,60)

calc_lat_boundaries()
calc_nl_table()

def nz(ctype):
	return 4 * latz - ctype

def dlat(ctype, surface):
	if surface == 0:
		tmp = 90.0
	else:
		tmp = 360.0

	return tmp / (4*latz - ctype)

def nl(declat_in):
	global nl_table

	declat_in_ = abs(int(math.floor(declat_in)))

	if declat_in_ == 0:
		return 59
	if declat_in_ == 87:
		return 2
	if declat_in_ > 87:
		return 1

	return nl_table[declat_in_]

def dlon(declat_in, ctype, surface):
	if surface == 0:
		tmp = 90.0
	else:
		tmp = 360.0

	cond = nl(rlat(declat_in, ctype, surface)) - ctype
	if cond > 0:
		tmp = tmp / cond

	return tmp

def YZ(declat, ctype, surface):
	global nb

	dlat_ = dlat(ctype,surface)
	yz = int(math.floor(2**nb[surface]*(declat % dlat_) / dlat_ + 0.5))
	if surface == 0:
		yz = yz % (2**17)

	return yz

def XZ(declat, declon, ctype, surface):
	global nb

	dlon_ = dlon(declat,ctype,surface)
	xz = int(math.floor(2**nb[surface]*(declon % dlon_) / dlon_ + 0.5))
	if surface == 0:
		xz = xz % (2**17)

	return xz

def rlat(declat, ctype, surface):
	global nb

	return int(dlat(ctype,surface) * (1.*YZ(declat,ctype,surface)/(2**nb[surface]) + math.floor(1.*declat/dlat(ctype,surface))))

def cpr_encode(lat, lon, ctype, surface):

	return (YZ(lat,ctype,surface), XZ(lat,lon,ctype,surface))

# def decode_lat(enclat, ctype, my_lat, surface):
# 	global nb
#
# 	tmp1 = dlat(ctype, surface)
# 	tmp2 = 1.*enclat/(2**nb[surface])
# 	j = math.floor(1.*my_lat/tmp1) + math.floor(0.5 + 1.*(my_lat % tmp1)/tmp1 - tmp2)
#
# 	return tmp1 * (j + tmp2)

# def decode_lon(declat, enclon, ctype, my_lon, surface):
# 	global nb
#
# 	tmp1 = dlon(declat, ctype, surface)
# 	tmp2 = 1.*enclon/(2**nb[surface])
# 	m = math.floor(1.*my_lon/tmp1) + math.floor(0.5 + 1.*(my_lon % tmp1)/tmp1 - tmp2)
#
# 	return tmp1 * (m + tmp2)

# def cpr_resolve_local(my_location, encoded_location, ctype, surface):
# 	[my_lat, my_lon] = my_location
# 	[enclat, enclon] = encoded_location
#
# 	decoded_lat = decode_lat(enclat, ctype, my_lat, surface)
# 	decoded_lon = decode_lon(decoded_lat, enclon, ctype, my_lon, surface)
#
# 	return (decoded_lat, decoded_lon)

# def cpr_resolve_global(evenpos, oddpos, my_pos, mostrecent, surface):
# 	dlateven = dlat(0, surface)
# 	dlatodd  = dlat(1, surface)
#
# 	# YZeven == evenpos[0]
# 	# YZodd == oddpos[0]
# 	j = math.floor(((59.*evenpos[0] - 60.*oddpos[0])/2**17) + 0.5)
#
# 	#print 'j even',j%60
# 	#print 'j odd',j%59
#
# 	rlateven = dlateven * ((j % (60-0)) + 1.*evenpos[0]/2**17)
# 	rlatodd  = dlatodd * ((j % (60-1)) + 1.*oddpos[0]/2**17)
#
# 	# limit to -90, 90
# 	if rlateven >= 270.0:
# 		rlateven -= 360.0
# 	if rlatodd >= 270.0:
# 		rlatodd -= 360.0
#
# 	#print 'dlateven',dlateven
# 	#print 'dlatodd',dlatodd
# 	#print 'rlateven',rlateven
# 	#print 'rlatodd',rlatodd
#
# 	if nl(rlateven) != nl(rlatodd):
# 		return None, None
#
# 	if mostrecent == 0:
# 		rlat = rlateven
# 	else:
# 		rlat = rlatodd
#
# 	# disambiguate latitude
# 	if surface == 0:
# 		if my_pos[0] < 0:
# 			assert rlat > 90
# 			rlat -= 90
#
# 	# _mr: most recent
# 	nl_rlat = nl(rlat)
# 	dlon_mr = dlon(rlat, mostrecent, surface)
#
# 	#print 'nl_rlat', nl_rlat
# 	#print 'dlon_mr', dlon_mr
#
# 	m = int(math.floor(((1.*evenpos[1]*(nl_rlat-1) - 1.*oddpos[1]*nl_rlat)/2**17) + 0.5))
# 	#print 'm',m
#
# 	if mostrecent == 0:
# 		XZ_mr = evenpos[1]
# 	else:
# 		XZ_mr = oddpos[1]
#
# 	rlon = dlon_mr * ((m % max(nl_rlat-mostrecent,1)) + 1.*XZ_mr/2**17)
#
# 	#print 'rlon', rlon
#
# 	# limit to -180, 180
# 	if rlon > 180:
# 		rlon -= 360
#
# 	# disambiguate longitude
# 	if surface == 0:
# 		b = int(my_pos[1]) / 90
# 		r = rlon % 90.
# 		rlon = b*90. + r
#
# 	#print 'rlon', rlon
#
# 	return (rlat, rlon)

# def decode(icao24, encoded_lat, encoded_lon, cpr_format, surface):
# 	global evenlist, oddlist
#
# 	if cpr_format == 0:
# 		evenlist[icao24] = [encoded_lat, encoded_lon, time.time()]
# 	else:
# 		oddlist[icao24] = [encoded_lat, encoded_lon, time.time()]
#
# 	if evenlist.has_key(icao24) and oddlist.has_key(icao24):
# 		time_interval = (oddlist[icao24][2] - evenlist[icao24][2])
# 		if abs(time_interval) < 10:
# 			newer = (time_interval > 0)
# 			return cpr_resolve_global(evenlist[icao24][0:2], oddlist[icao24][0:2], newer, surface)
#
# 	return None, None

coordenadas = cpr_encode(52.25720, 3.91937, 0, 1)
latitude = coordenadas[0]
longitude = coordenadas[1]

print (coordenadas)
