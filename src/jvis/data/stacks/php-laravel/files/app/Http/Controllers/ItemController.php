<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreItemRequest;
use App\Http\Requests\UpdateItemRequest;
use App\Models\Item;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Response;

class ItemController extends Controller
{
    public function index(): JsonResponse
    {
        $items = Item::orderBy('created_at', 'desc')->get();

        return response()->json($items);
    }

    public function store(StoreItemRequest $request): JsonResponse
    {
        $item = Item::create($request->validated());

        return response()->json($item, Response::HTTP_CREATED);
    }

    public function show(Item $item): JsonResponse
    {
        return response()->json($item);
    }

    public function update(UpdateItemRequest $request, Item $item): JsonResponse
    {
        $item->update($request->validated());

        return response()->json($item);
    }

    public function destroy(Item $item): Response
    {
        $item->delete();

        return response()->noContent();
    }
}
