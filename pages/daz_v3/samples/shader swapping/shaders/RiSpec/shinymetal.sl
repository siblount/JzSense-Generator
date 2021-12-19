surface
shinymetal(
	float Ka = 1;
	float Ks = 1;
	float Kr = 1;
	float roughness = .1;
	string texturename = "" )
{
	normal Nf = faceforward( normalize( N ), I );
	vector V = normalize( -I );
	point D;
	color Ckr;

	D = reflect( I, normalize( Nf ) );
	D = transform( "world", point "world" ( 0, 0, 0 ) + D );
	// Account for differences in coordinate system and axis orientation
	D = point( comp( D, 2 ), comp( D, 0 ), comp( D, 1 ) );
	
	Ckr = ( texturename != "" ) ? environment( texturename, D ) : 0.0;

	Oi = Os;
	Ci = Os * Cs * ( ( Ka * ambient() ) + ( Ks * specular( Nf, V, roughness ) ) + ( Kr * Ckr ) );
}
