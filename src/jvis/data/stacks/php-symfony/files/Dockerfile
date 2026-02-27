FROM php:8.3-fpm AS base

RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libpq-dev \
    libicu-dev \
    zip \
    unzip \
    && docker-php-ext-configure intl \
    && docker-php-ext-install pdo pdo_mysql pdo_pgsql mbstring exif pcntl bcmath gd intl opcache \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

FROM base AS development
ENV APP_ENV=dev
COPY composer.json composer.lock* ./
RUN composer install --no-scripts --no-autoloader
COPY . .
RUN composer dump-autoload --optimize
RUN php bin/console cache:warmup
EXPOSE 8000
CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]

FROM base AS production
ENV APP_ENV=prod
COPY composer.json composer.lock* ./
RUN composer install --no-dev --no-scripts --no-autoloader --optimize-autoloader
COPY . .
RUN composer dump-autoload --optimize --no-dev --classmap-authoritative
RUN php bin/console cache:warmup --env=prod
RUN chown -R www-data:www-data /var/www/html/var
EXPOSE 9000
CMD ["php-fpm"]
