<?php

namespace App\Controller;

use App\Entity\Item;
use App\Repository\ItemRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/items')]
class ItemController extends AbstractController
{
    public function __construct(
        private readonly EntityManagerInterface $em,
        private readonly ItemRepository $repository,
    ) {
    }

    #[Route('', methods: ['GET'])]
    public function index(): JsonResponse
    {
        $items = $this->repository->findAllOrderedByDate();

        return $this->json(array_map(fn (Item $item) => $this->serialize($item), $items));
    }

    #[Route('', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['name'])) {
            return $this->json(['error' => 'name is required'], Response::HTTP_BAD_REQUEST);
        }

        $item = new Item();
        $item->setName($data['name']);
        $item->setDescription($data['description'] ?? null);

        $this->em->persist($item);
        $this->em->flush();

        return $this->json($this->serialize($item), Response::HTTP_CREATED);
    }

    #[Route('/{id}', methods: ['GET'])]
    public function show(string $id): JsonResponse
    {
        $item = $this->repository->find($id);

        if (!$item) {
            return $this->json(['error' => 'Item not found'], Response::HTTP_NOT_FOUND);
        }

        return $this->json($this->serialize($item));
    }

    #[Route('/{id}', methods: ['PATCH'])]
    public function update(string $id, Request $request): JsonResponse
    {
        $item = $this->repository->find($id);

        if (!$item) {
            return $this->json(['error' => 'Item not found'], Response::HTTP_NOT_FOUND);
        }

        $data = json_decode($request->getContent(), true);

        if (isset($data['name'])) {
            $item->setName($data['name']);
        }
        if (array_key_exists('description', $data)) {
            $item->setDescription($data['description']);
        }

        $this->em->flush();

        return $this->json($this->serialize($item));
    }

    #[Route('/{id}', methods: ['DELETE'])]
    public function delete(string $id): Response
    {
        $item = $this->repository->find($id);

        if (!$item) {
            return $this->json(['error' => 'Item not found'], Response::HTTP_NOT_FOUND);
        }

        $this->em->remove($item);
        $this->em->flush();

        return new Response(null, Response::HTTP_NO_CONTENT);
    }

    private function serialize(Item $item): array
    {
        return [
            'id' => (string) $item->getId(),
            'name' => $item->getName(),
            'description' => $item->getDescription(),
            'createdAt' => $item->getCreatedAt()?->format(\DateTimeInterface::ATOM),
            'updatedAt' => $item->getUpdatedAt()?->format(\DateTimeInterface::ATOM),
        ];
    }
}
