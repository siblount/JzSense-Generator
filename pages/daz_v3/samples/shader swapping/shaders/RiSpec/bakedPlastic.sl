surface
bakedPlastic(
	float Ka = 1;
	float Kd = .5;
	float Ks = .5;
	float roughness = .1;
	color specularcolor = 1;
	string BakeFileName = "";
	string BakeType = "";
 )
{
	normal Nf = faceforward( normalize( N ), I );
	vector V = normalize( -I );
	
	Oi = Os;
	
	if(BakeFileName!="")
	{
		color colorToBake = 0;
		if(BakeType=="Illumination")
		{
			colorToBake = ( ( Ka * ambient() ) + ( Kd * diffuse( Nf ) ) ) +
			( specularcolor * Ks * specular( Nf, V, roughness ) );
		}
		else if(BakeType=="Shader")
		{
			colorToBake = Cs;
		}
		else if(BakeType=="IllumShader")
		{
			colorToBake = Cs * ( ( Ka * ambient() ) + ( Kd * diffuse( Nf ) ) ) +
			( specularcolor * Ks * specular( Nf, V, roughness ) );
		}
		bake(BakeFileName,s,t,colorToBake);
	}
	
	Ci = Os * ( Cs * ( ( Ka * ambient() ) + ( Kd * diffuse( Nf ) ) ) +
		( specularcolor * Ks * specular( Nf, V, roughness ) ) );
}
