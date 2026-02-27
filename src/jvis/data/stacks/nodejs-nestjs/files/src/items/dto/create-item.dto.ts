import { IsString, IsNotEmpty, IsOptional, MinLength } from 'class-validator';

export class CreateItemDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(1)
  name!: string;

  @IsString()
  @IsOptional()
  description?: string | null;
}
