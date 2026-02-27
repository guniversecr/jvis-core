<?php

use App\Http\Controllers\HealthController;
use App\Http\Controllers\ItemController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group.
|
*/

Route::get('/health', [HealthController::class, 'index'])
    ->name('health.index');

Route::apiResource('items', ItemController::class);

Route::middleware('auth:sanctum')->group(function () {
    // Authenticated API routes go here
});
