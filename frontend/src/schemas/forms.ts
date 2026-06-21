import { z } from 'zod'

export const loginSchema = z.object({
  login: z.string().min(1, 'Informe o login.'),
  senha: z.string().min(1, 'Informe a senha.')
})

export const hospedeSchema = z.object({
  nome: z.string().min(2, 'Informe o nome.'),
  cpf: z.string().regex(/^\d{11}$/, 'Informe apenas os 11 números do CPF.'),
  telefone: z.string().optional(),
  email: z.string().email('E-mail inválido.').optional().or(z.literal(''))
})

export const tipoQuartoSchema = z.object({
  descricao: z.string().min(2, 'Informe a descrição.'),
  preco_base: z.coerce.number().positive('Informe um preço positivo.'),
  capacidade: z.coerce.number().int().positive('Informe a capacidade.'),
  ativo: z.boolean()
})

export const quartoSchema = z.object({
  numero: z.string().min(1, 'Informe o número.'),
  tipo_id: z.coerce.number().positive('Selecione o tipo.'),
  status_id: z.coerce.number().positive('Selecione o status.'),
  observacoes: z.string().optional(),
  ativo: z.boolean()
})

export const reservaSchema = z
  .object({
    data_entrada: z.string().min(1, 'Informe a entrada.'),
    data_saida: z.string().min(1, 'Informe a saída.'),
    quantidade_hospedes: z.coerce.number().int().positive('Informe a quantidade.'),
    hospede_id: z.coerce.number().positive('Selecione o hóspede.'),
    quarto_numero: z.string().min(1, 'Selecione o quarto.'),
    observacoes: z.string().optional()
  })
  .refine((data) => data.data_saida > data.data_entrada, {
    message: 'A saída deve ser posterior à entrada.',
    path: ['data_saida']
  })

export const pagamentoSchema = z.object({
  reserva_id: z.coerce.number().positive('Selecione a reserva.'),
  metodo_id: z.coerce.number().positive('Selecione o método.'),
  valor: z.coerce.number().positive('Informe um valor positivo.'),
  observacoes: z.string().optional()
})

export const usuarioSchema = z.object({
  nome: z.string().min(2, 'Informe o nome.'),
  login: z.string().min(3, 'Informe o login.'),
  senha: z.string().min(6, 'Senha mínima de 6 caracteres.'),
  perfil_id: z.coerce.number().positive('Selecione o perfil.'),
  ativo: z.boolean()
})
