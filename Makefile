bsae:
	docker build -f CI/base.Dockerfile \
	-t angora-dsl-base:latest \
	--compress \
	--no-cache \
	.

ci:
	docker build -f CI/ci.Dockerfile \
	-t angora-dsl:latest \
	--compress \
	--no-cache \
	.
