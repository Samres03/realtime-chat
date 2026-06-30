package types

type Env struct {
	Jwt EnvJwt
	Db EnvDb
}

type EnvJwt struct {
	SecretKey string 
	Algorithm string
	AccessTokenExpireMinutes int
}

type EnvDb struct {
	Url string
}
