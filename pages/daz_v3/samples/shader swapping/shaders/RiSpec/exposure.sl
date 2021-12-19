imager
exposure( float gain=1.0, gamma=1.0, one = 255, min = 0, max = 255 )
{
	Ci = pow( gain * Ci, 1/gamma );
	Ci = clamp( round( one * Ci ), min, max );
	Oi = clamp( round( one * Oi ), min, max );
}